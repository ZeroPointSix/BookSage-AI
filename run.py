import os, sys, subprocess, venv

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(ROOT, ".venv")
PY = os.path.join(VENV, "Scripts", "python.exe") if os.name == "nt" else os.path.join(VENV, "bin", "python")

def kill_on_port(port):
    if os.name == "nt":
        # Find PIDs for the port
        cmd = f"netstat -ano | findstr LISTENING | findstr :{port}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        pids = set(re.findall(r"\s(\d+)$", res.stdout, re.M))
        for pid in pids:
            if pid != "0":
                subprocess.run(f"taskkill /F /T /PID {pid}", shell=True, capture_output=True)

if sys.executable.lower() != PY.lower():
    if not os.path.exists(VENV):
        print("--- Creating Virtual Environment ---")
        venv.create(VENV, with_pip=True)
    # Use call instead of run to ensure output flows correctly
    subprocess.call([PY, __file__] + sys.argv[1:])
    sys.exit()

import re # Import here inside venv for cleanliness

print("\n--- BookSage-AI Setup ---")

print("Cleaning up ports 8000 & 5173...")
for port in [8000, 5173]: kill_on_port(port)

print("Checking dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], capture_output=True)

if not os.path.exists("frontend/node_modules"):
    print("Installing frontend dependencies...")
    subprocess.run("cmd /c npm install" if os.name == "nt" else "npm install", cwd="frontend", shell=True)

if not os.path.exists("backend/app/models/cf_model.pkl"):
    if input("\nRecommendation models missing. Train? (y/N): ").lower() == 'y':
        subprocess.run([sys.executable, "app/train_models.py"], cwd="backend")

print("\nStarting Services...")
backend = subprocess.Popen([sys.executable, "run.py", "--prod"], cwd="backend", shell=True)
frontend = subprocess.Popen("cmd /c npm run dev" if os.name == "nt" else "npm run dev", cwd="frontend", shell=True)

print("Backend: http://127.0.0.1:8000 | Frontend: http://localhost:5173\n")

try:
    backend.wait()
except KeyboardInterrupt:
    print("\nStopping...")
    if os.name == "nt":
        for p in [backend, frontend]: subprocess.run(f"taskkill /F /T /PID {p.pid}", capture_output=True)
    else:
        for p in [backend, frontend]: p.terminate()
    print("Stopped.")
