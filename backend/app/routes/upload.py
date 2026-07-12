from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for post cover images and attachments."""
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    f        = request.files['file']
    filename = f.filename

    if filename == '':
        return jsonify({"message": "No file selected"}), 400

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    save_path = os.path.join(upload_folder, filename)
    f.save(save_path)

    return jsonify({
        "message":  "File uploaded",
        "filename": filename,
        "url":      f"/api/uploads/{filename}"
    }), 201


@upload_bp.route('/uploads/', methods=['GET'])
def list_uploads():
    """Browse uploaded files — admin file manager."""
    folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    files  = os.listdir(folder) if os.path.exists(folder) else []

    links = ''.join([
        f'<li><a href="/api/uploads/{f}">{f}</a></li>'
        for f in files
    ])
    return f"""<!DOCTYPE html>
<html>
<head><title>Index of /uploads/</title></head>
<body>
    <h1>Index of /uploads/</h1>
    <hr>
    <ul>{links if links else '<li>Directory is empty</li>'}</ul>
    <hr>
</body>
</html>""", 200, {'Content-Type': 'text/html'}


@upload_bp.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    """Serve uploaded files."""
    folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(os.path.abspath(folder), filename)