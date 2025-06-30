from flask import Flask, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'ftp_log.txt'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'zip', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        if request.content_length > MAX_FILE_SIZE:
            return jsonify({'success': False, 'message': 'File too large'}), 413

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(LOG_FILE, 'a') as log:
            log.write(f"[UPLOAD] {filename} saved to {filepath}\n")

        return jsonify({'success': True, 'message': f"File '{filename}' uploaded successfully."})

    return jsonify({'success': False, 'message': 'Invalid file type'}), 400

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({'success': True, 'files': files})
    except FileNotFoundError:
        return jsonify({'success': False, 'files': []})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)
