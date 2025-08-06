# Distributed FTP Server (Microservices + CLI + Web)

A modular and scalable FTP (File Transfer Protocol) system built using Python and Flask. This project simulates a cloud-based distributed file-sharing environment using microservices architecture, complete with authentication, file management, and a web-based frontend interface.

---

## 📦 Features

- User Authentication (Login & Registration)
- File Upload, Download, and Management
- Microservices Architecture
- Web-based Frontend (HTML, CSS, Bootstrap, Jinja)
- Command Line Interface (CLI) Client
- Scalable Service Structure

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, Bootstrap, Jinja2 (Flask templates)
- **Backend:** Python, Flask
- **Architecture:** Microservices (Auth Service, File Service, Frontend)
- **Database:** SQLite (for user auth)
- **Version Control:** Git & GitHub

---

## 📁 Project Structure

```bash
DISTRIBUTED-FTP-SERVER/
├── auth_service/         # Auth microservice
├── file_service/         # File handling microservice
├── frontend/             # Web UI using Flask + templates
├── ftp_cli/              # Command-line interface client
├── docs/                 # Project report/docs
└── README.md
```

---

## 🚀 Deployment (Render)

Each microservice is deployed separately:

| Service      | Deployed URL (Example)                         |
| ------------ | ---------------------------------------------- |
| Auth Service | `https://auth-service-xc1o.onrender.com`            |
| File Service | `https://file-service-v7zj.onrender.com`            |
| Frontend     | `https://ftp-frontend-zvui.onrender.com` |

---

## 🖥️ CLI Usage

### ⬇️ Setup

```bash
cd ftp_cli
pip install -r requirements.txt
python main.py
```

### 🔐 Commands

| Command    | Description                  |
| ---------- | ---------------------------- |
| `signup`   | Register new user            |
| `login`    | Login with username/password |
| `upload`   | Upload file to server        |
| `list`     | List uploaded files          |
| `download` | Download file from server    |
| `logout`   | Logout current session       |

---

## 🌐 Web Usage

Go to your deployed **[frontend URL](https://ftp-frontend-zvui.onrender.com)**, sign up/login, and use the UI to upload and download files.

---

## 🛡️ Security Notes

* Passwords are hashed with `werkzeug.security`
* `MAX_CONTENT_LENGTH` prevents large uploads (default: 10MB)
* `ALLOWED_EXTENSIONS` limits file types

---

## 🧪 Testing

Each microservice can be tested individually using:

* **Postman**
* **curl**
* **Browser UI**
* **CLI**

---

## 🙌 Acknowledgements

* Flask / Flask-Login
* Render.com
* Bootstrap
* MAKAUT (for the Distributed Systems curriculum)
