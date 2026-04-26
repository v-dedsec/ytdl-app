import os
import re
import threading
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Track job progress
jobs = {}


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)


def download_job(job_id, url, mode):
    """Run in background thread."""
    try:
        jobs[job_id]["status"] = "downloading"

        if mode == "mp3":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, f"{job_id}.%(ext)s"),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
                "no_warnings": True,
            }
        else:
            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, f"{job_id}.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = sanitize_filename(info.get("title", "video"))

        # Find the output file
        ext = "mp3" if mode == "mp3" else "mp4"
        filename = f"{job_id}.{ext}"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        # yt-dlp may use a different extension; search for it
        if not os.path.exists(filepath):
            for f in os.listdir(DOWNLOAD_FOLDER):
                if f.startswith(job_id):
                    filename = f
                    filepath = os.path.join(DOWNLOAD_FOLDER, f)
                    break

        jobs[job_id].update({
            "status": "done",
            "filename": filename,
            "title": title,
        })

    except Exception as e:
        jobs[job_id].update({"status": "error", "error": str(e)})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    data = request.json
    url = data.get("url", "").strip()
    mode = data.get("mode", "video")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "queued"}

    thread = threading.Thread(target=download_job, args=(job_id, url, mode), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id})


@app.route("/status/<job_id>")
def status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
