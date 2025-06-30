from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
USER_FILE = 'users.json'

# Load users from file
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists.'}), 400

    users[username] = generate_password_hash(password)
    save_users(users)
    return jsonify({'success': True, 'message': 'User registered successfully.'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    if username in users and check_password_hash(users[username], password):
        return jsonify({'success': True, 'message': 'Login successful.'})
    return jsonify({'success': False, 'message': 'Invalid credentials.'}), 401

if __name__ == '__main__':
    app.run(port=5001, debug=True)
