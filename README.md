# TubeGrab — YouTube Downloader + MP3 Converter

A clean Flask web app to download YouTube videos (MP4) or extract audio (MP3).

---

## Run Locally

### Requirements
- Python 3.9+
- `ffmpeg` installed on your system

### Install ffmpeg
- **Ubuntu/Debian**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/download.html and add to PATH

### Setup & Run
```bash
pip install -r requirements.txt
python app.py
```
Then open http://localhost:5000

---

## Free Hosting Options

### Option 1 — Railway (Recommended, Easiest)
1. Push this folder to a GitHub repo
2. Go to https://railway.app → Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo → Railway auto-detects Flask + Procfile
5. Add environment variable: `PORT=5000`
6. Click Deploy — you get a free `.railway.app` URL!

> Note: Railway gives $5/month free credit (enough for small apps)

### Option 2 — Render.com
1. Push to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your GitHub repo
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Deploy! Free tier spins down after inactivity (cold start ~30s)

### Option 3 — PythonAnywhere (Forever Free)
1. Sign up at https://www.pythonanywhere.com (free tier)
2. Go to "Files" → upload all project files
3. Go to "Web" → Add new web app → Flask
4. Set source directory to your project folder
5. In the WSGI file, point it to `app.py`
6. Note: ffmpeg may need to be installed manually (contact their support)

### Option 4 — Fly.io (Free Tier)
1. Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
2. Run `fly launch` in your project folder
3. Run `fly deploy`
4. Free: 3 shared VMs + 3GB storage

---

## Project Structure
```
ytdl-app/
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── Procfile            # For Railway/Render
├── templates/
│   └── index.html      # Frontend UI
└── static/
    └── downloads/      # Downloaded files (auto-created)
```

## Notes
- Downloaded files are saved in `static/downloads/`
- For production, add a cleanup job to delete old files
- Some videos may be age-restricted or region-locked
