# TubeGrab 🎬

> A clean, fast YouTube video downloader and MP3 converter built with Python & Flask.

**Author:** v-dedsec

---

## Features

- 🎬 **Download YouTube videos** in best available MP4 quality
- 🎵 **Convert to MP3** — extracts audio at 192kbps
- 🤖 **Anti-bot bypass** — tries multiple YouTube clients (Android, TV, iOS) automatically so no login is needed
- ⚡ **Background downloads** — non-blocking, shows live status while downloading
- 🎨 **Clean dark UI** — no ads, no sign-up, just paste and download
- 🔁 **Auto-retry** — if one method fails it silently tries the next one

---

## Run Locally

### Requirements
- Python 3.9+
- ffmpeg installed on your system

### Install ffmpeg

**Ubuntu / Debian**
```bash
sudo apt install ffmpeg
```

**macOS**
```bash
brew install ffmpeg
```

**Windows**
Download from https://ffmpeg.org/download.html and add to PATH

### Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/v-dedsec/ytdl-app.git
cd ytdl-app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open your browser and go to:
```
http://localhost:8080
```

---

## ⚠️ Hosting Warning

If you try to host this on a cloud platform (Railway, Render, etc.) and use it from there, **things may not work properly:**

- YouTube actively blocks downloads from server/cloud IP addresses
- You will likely get errors like *"Sign in to confirm you're not a bot"* or *"Failed to extract player response"*
- The anti-bot bypass helps but is not guaranteed on cloud servers since YouTube constantly updates its detection
- Downloaded files are stored in memory/disk temporarily and may be lost on server restarts
- Free tier servers have limited CPU/RAM which can cause timeouts on large videos

**Running locally works perfectly with no issues** since your home IP is not flagged by YouTube.

---

## Tech Stack

- **Python** — core language
- **Flask** — web framework
- **yt-dlp** — YouTube downloading engine
- **ffmpeg** — audio conversion
- **gunicorn** — production server (for hosting only)

---

*Made by v-dedsec*
