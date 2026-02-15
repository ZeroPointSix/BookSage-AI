import subprocess
import sys
import os

# Kill existing processes on ports
subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq *uvicorn*\" 2>nul", shell=True, capture_output=True)
subprocess.run("taskkill /F /FI \"WINDOWTITLE eq *vite*\" 2>nul", shell=True, capture_output=True)

root = os.path.dirname(os.path.abspath(__file__))

print("Starting BookSage-AI...")
print("-" * 50)

# Start backend and frontend
backend = subprocess.Popen([sys.executable, "run.py", "--prod"], cwd=f"{root}/backend", shell=True)
frontend = subprocess.Popen(["npm", "run", "dev"], cwd=f"{root}/frontend", shell=True)

print("\nServices started!")
print("Backend:  http://127.0.0.1:8000")
print("Frontend: http://localhost:5173")
print("\nPress Ctrl+C to stop.\n")

try:
    backend.wait()
except KeyboardInterrupt:
    print("\n\nStopping services...")
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(backend.pid)], capture_output=True)
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(frontend.pid)], capture_output=True)
    print("Stopped successfully!")
