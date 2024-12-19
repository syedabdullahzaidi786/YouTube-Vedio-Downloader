from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Download Video
@app.route("/download", methods=["POST"])
def download_video():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    options = {
        "format": "best",  # Simple best video/audio download
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
    }

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return jsonify({"success": True, "filename": os.path.basename(filename)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve Downloaded Files
@app.route("/downloads/<filename>")
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
