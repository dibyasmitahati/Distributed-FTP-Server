import requests
import os
import json

AUTH_URL = 'http://localhost:5001'
FILE_URL = 'http://localhost:5002'
CONFIG_FILE = 'config.json'

# Load saved session from file
def load_session():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

# Save session to file
def save_session(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f)

# Clear session
def logout():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    print("🔓 Logged out.")

session = load_session()

def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    res = requests.post(f'{AUTH_URL}/register', json={'username': username, 'password': password})
    msg = res.json().get('message', '')
    print("[📝]", msg)

def login():
    username = input("Username: ")
    password = input("Password: ")
    res = requests.post(f'{AUTH_URL}/login', json={'username': username, 'password': password})
    if res.status_code == 200:
        session['username'] = username
        save_session(session)
        print("[✅] Login successful.")
    else:
        print("[❌] Login failed:", res.json().get('message'))

def upload_file():
    if 'username' not in session:
        print("Please login first.")
        return
    path = input("Path to file: ").strip()
    if not os.path.isfile(path):
        print("[❌] File does not exist.")
        return
    with open(path, 'rb') as f:
        files = {'file': (os.path.basename(path), f)}
        try:
            res = requests.post(f'{FILE_URL}/upload', files=files)
            print("[📤]", res.json().get('message'))
        except Exception as e:
            print("[❌] Upload failed:", str(e))

def list_files():
    try:
        res = requests.get(f'{FILE_URL}/files')
        files = res.json().get('files', [])
        if files:
            print("[📃] Files on server:")
            for f in files:
                print(" -", f)
        else:
            print("[📂] No files available.")
    except:
        print("[❌] Failed to fetch file list.")

def download_file():
    filename = input("Enter file name to download: ").strip()
    try:
        res = requests.get(f'{FILE_URL}/download/{filename}', stream=True)
        if res.status_code == 200:
            out_path = f"downloads/{filename}"
            os.makedirs('downloads', exist_ok=True)
            with open(out_path, 'wb') as f:
                f.write(res.content)
            print(f"[📥] Downloaded to {out_path}")
        else:
            print("[❌] File not found.")
    except Exception as e:
        print("[❌] Download error:", str(e))

def main():
    print("📡 Distributed FTP CLI")
    while True:
        print("\nOptions:")
        print("1. Signup")
        print("2. Login")
        print("3. Upload File")
        print("4. List Files")
        print("5. Download File")
        print("6. Logout")
        print("7. Exit")
        choice = input("Select: ").strip()

        if choice == '1':
            signup()
        elif choice == '2':
            login()
        elif choice == '3':
            upload_file()
        elif choice == '4':
            list_files()
        elif choice == '5':
            download_file()
        elif choice == '6':
            logout()
        elif choice == '7':
            print("👋 Exiting FTP CLI.")
            break
        else:
            print("❓ Invalid choice.")

if __name__ == "__main__":
    main()
