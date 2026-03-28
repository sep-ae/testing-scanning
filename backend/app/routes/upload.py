from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os

upload_bp = Blueprint('upload', __name__)

# ============ UPLOAD VULNERABLE ============
# Tidak ada validasi ekstensi, tidak ada auth

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    f        = request.files['file']
    filename = f.filename  # langsung pakai nama dari user — path traversal vuln juga!

    if filename == '':
        return jsonify({"message": "No file selected"}), 400

    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    save_path = os.path.join(upload_folder, filename)
    f.save(save_path)

    return jsonify({
        "message": "File uploaded",
        "filename": filename,
        "url": f"/api/uploads/{filename}"
    }), 201


# ============ DIRECTORY LISTING VULNERABLE ============

@upload_bp.route('/uploads/', methods=['GET'])
def list_uploads():
    folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    if not os.path.exists(folder):
        files = []
    else:
        files = os.listdir(folder)

    # Sengaja return HTML dengan directory listing
    links = ''.join([
        f'<li><a href="/api/uploads/{f}">{f}</a></li>'
        for f in files
    ])
    return f'''<!DOCTYPE html>
<html>
<head><title>Index of /uploads/</title></head>
<body>
    <h1>Index of /uploads/</h1>
    <hr>
    <ul>{links if links else '<li>Directory kosong</li>'}</ul>
    <hr>
</body>
</html>''', 200, {'Content-Type': 'text/html'}


# ============ SERVE FILE ============

@upload_bp.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(os.path.abspath(folder), filename)