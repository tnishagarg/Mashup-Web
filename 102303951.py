import sys
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment


# ---------------------------
# Function to download videos
# ---------------------------
def download_videos(singer, num_videos):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
    'format': 'bestaudio[ext=m4a]/bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'quiet': False,
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


# ---------------------------
# Function to create mashup
# ---------------------------
def create_mashup(duration, output_file):
    combined = AudioSegment.empty()

    files = os.listdir("downloads")

    if not files:
        print("No files found in downloads folder.")
        sys.exit(1)

    for file in files:
        file_path = os.path.join("downloads", file)

        try:
            audio = AudioSegment.from_file(file_path)
            trimmed = audio[:duration * 1000]  # seconds → milliseconds
            combined += trimmed
            print(f"Processed: {file}")
        except Exception as e:
            print(f"Skipping {file} due to error: {e}")

    combined.export(output_file, format="mp3")


# ---------------------------
# Main Function
# ---------------------------
def main():

    # Check correct number of arguments
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]

    # Validate integers
    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Error: NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    output_file = sys.argv[4]

    # Validate conditions
    if num_videos <= 10:
        print("Error: Number of videos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("Error: Audio duration must be greater than 20 seconds.")
        sys.exit(1)

    try:
        print("\nDownloading videos...")
        download_videos(singer, num_videos)

        print("\nCreating mashup...")
        create_mashup(duration, output_file)

        print("\nMashup created successfully!")
        print("Output file:", output_file)

    except Exception as e:
        print("An unexpected error occurred:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
