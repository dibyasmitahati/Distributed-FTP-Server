from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key'

AUTH_URL = 'http://localhost:5001'
FILE_URL = 'http://localhost:5002'

# Home Page
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Get file list from file service
    try:
        response = requests.get(f'{FILE_URL}/files')
        files = response.json().get('files', [])
    except:
        files = []
        flash('Could not fetch files.')

    return render_template('index.html', username=session['user'], files=files)

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password']
        }
        res = requests.post(f'{AUTH_URL}/register', json=data)
        msg = res.json().get('message', '')
        flash(msg)
        if res.status_code == 200:
            return redirect(url_for('login'))
    return render_template('signup.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password']
        }
        res = requests.post(f'{AUTH_URL}/login', json=data)
        msg = res.json().get('message', '')
        if res.status_code == 200:
            session['user'] = data['username']
            return redirect(url_for('index'))
        flash(msg)
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Upload File
@app.route('/upload', methods=['POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    file = request.files.get('file')
    if file:
        try:
            files = {'file': (file.filename, file.stream, file.content_type)}
            res = requests.post(f'{FILE_URL}/upload', files=files)
            flash(res.json().get('message', 'Upload failed.'))
        except:
            flash('Upload service not responding.')
    else:
        flash('No file selected.')
    return redirect(url_for('index'))

# Download File
@app.route('/download/<filename>')
def download(filename):
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        file_res = requests.get(f'{FILE_URL}/download/{filename}', stream=True)
        if file_res.status_code == 200:
            temp_path = f'temp/{filename}'
            os.makedirs('temp', exist_ok=True)
            with open(temp_path, 'wb') as f:
                f.write(file_res.content)
            return send_file(temp_path, as_attachment=True)
        flash("File not found.")
    except:
        flash("File service unavailable.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
