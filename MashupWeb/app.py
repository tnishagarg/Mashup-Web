from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer = request.form["singer"]
        num_videos = request.form["videos"]
        duration = request.form["duration"]
        email = request.form["email"]

        response = requests.post(
            f"{BACKEND_URL}/process",
            json={
                "singer": singer,
                "videos": num_videos,
                "duration": duration,
                "email": email
            }
        )

        return response.text

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
