# Mashup Web Application

A Flask-based web application that generates audio mashups from YouTube videos.  
Users can provide YouTube URLs, and the app downloads, processes, and combines audio clips into a mashup.

**Live Demo:** https://mashup-web-jzcz.onrender.com/

---

## Features

- Download audio from YouTube using yt-dlp  
- Trim and process audio clips  
- Combine multiple audio files into one mashup  
- Simple and interactive web interface  
- Deployed on Render  

---

## Tech Stack

- Python 3.11  
- Flask  
- Gunicorn  
- yt-dlp  
- pydub  
- moviepy  
- HTML / CSS  

---

## Project Structure

```
Mashup-Web/
│
├── MashupWeb/
│   ├── app.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
│
├── .python-version
├── 102303951.py
└── README.md

```

---

## Installation (Run Locally)

### 1️. Clone the repository

```bash
git clone https://github.com/tnishagarg/Mashup-Web.git
cd Mashup-Web
```

### 2️. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️. Install dependencies

```bash
pip install -r MashupWeb/requirements.txt
```

### 4️. Run the application

```bash
python MashupWeb/app.py
```

Open in your browser:

```
http://127.0.0.1:5000
```

---

## Deployment (Render)

- **Build Command**
  ```
  pip install -r MashupWeb/requirements.txt
  ```

- **Start Command**
  ```
  gunicorn MashupWeb.app:app
  ```

- **Python Version**
  ```
  3.11.9
  ```

---

## Important Notes

- Python 3.11 is required (Python 3.13+ removes `audioop`, which is required by `pydub`).
- FFmpeg must be installed for audio processing.
- Ensure YouTube URLs are public and valid.

---
