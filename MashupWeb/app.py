from flask import Flask, render_template, request
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
import zipfile
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

def create_mashup(singer, num_videos, duration, output_file):

    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android']
            }
        }
    }

    search_query = f"ytsearch{num_videos}:{singer} songs"

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

    combined = AudioSegment.empty()

    for file in os.listdir("downloads"):
        file_path = os.path.join("downloads", file)
        audio = AudioSegment.from_file(file_path)
        trimmed = audio[:duration * 1000]
        combined += trimmed

    combined.export(output_file, format="mp3")

    # Zip file
    zip_name = "mashup.zip"
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(output_file)

    return zip_name


def send_email(receiver_email, zip_file):

    sender_email = os.getenv("SENDER_EMAIL")
    app_password = os.getenv("APP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("Attached is your mashup file.")

    with open(zip_file, "rb") as f:
        msg.add_attachment(f.read(),
                           maintype="application",
                           subtype="zip",
                           filename=zip_file)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form["singer"]
        num_videos = int(request.form["videos"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        if num_videos <= 10 or duration <= 20:
            return "Videos must be >10 and duration >20"

        zip_file = create_mashup(singer, num_videos, duration, "output.mp3")
        send_email(email, zip_file)

        return "Mashup created and sent to your email!"

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

