# run_all.py
import subprocess
import os
import time

base_path = os.getcwd()

# Start auth_service
subprocess.Popen(["python", "app.py"], cwd=os.path.join(base_path, "auth_service"))

# Start file_service
subprocess.Popen(["python", "app.py"], cwd=os.path.join(base_path, "file_service"))

# Start frontend (last)
time.sleep(2)
subprocess.Popen(["python", "app.py"], cwd=os.path.join(base_path, "frontend"))
