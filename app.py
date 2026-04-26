import os
import re
import threading
import uuid
from flask import Flask, request, jsonify, send_from_directory, render_template
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

jobs = {}


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)


def download_job(job_id, url, mode):
    try:
        jobs[job_id]["status"] = "downloading"

        outtmpl = os.path.join(DOWNLOAD_FOLDER, f"{job_id}.%(ext)s")

        # Try multiple client strategies in order until one works
        strategies = [
            {
                "extractor_args": {"youtube": {"player_client": ["android"]}},
            },
            {
                "extractor_args": {"youtube": {"player_client": ["tv_embedded"]}},
            },
            {
                "extractor_args": {"youtube": {"player_client": ["ios"]}},
            },
            {
                # Last resort - no special client
                "extractor_args": {},
            },
        ]

        base = {
            "quiet": True,
            "no_warnings": True,
            "outtmpl": outtmpl,
            "http_headers": {
                "User-Agent": "com.google.android.youtube/17.36.4 (Linux; U; Android 12; GB) gzip",
            },
            "socket_timeout": 30,
        }

        if mode == "mp3":
            base["format"] = "bestaudio/best"
            base["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        else:
            base["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

        last_error = None
        for strategy in strategies:
            try:
                opts = {**base, **strategy}
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = sanitize_filename(info.get("title", "video"))

                # Find output file
                ext = "mp3" if mode == "mp3" else "mp4"
                filename = f"{job_id}.{ext}"
                if not os.path.exists(os.path.join(DOWNLOAD_FOLDER, filename)):
                    for f in os.listdir(DOWNLOAD_FOLDER):
                        if f.startswith(job_id):
                            filename = f
                            break

                jobs[job_id].update({"status": "done", "filename": filename, "title": title})
                return  # success — stop trying

            except Exception as e:
                last_error = e
                continue  # try next strategy

        # All strategies failed
        jobs[job_id].update({"status": "error", "error": f"Could not download video. YouTube may be blocking server downloads. Try a different video. ({last_error})"})

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
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
