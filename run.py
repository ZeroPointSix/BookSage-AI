import subprocess
import sys
import os

# Kill existing processes on ports
subprocess.run("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq *uvicorn*\" 2>nul", shell=True, capture_output=True)
subprocess.run("taskkill /F /FI \"WINDOWTITLE eq *vite*\" 2>nul", shell=True, capture_output=True)

root = os.path.dirname(os.path.abspath(__file__))

def check_dependencies():
    """Ensure all dependencies are installed."""
    # 1. Check Frontend (node_modules)
    frontend_path = os.path.join(root, "frontend")
    node_modules = os.path.join(frontend_path, "node_modules")
    
    if not os.path.exists(node_modules):
        print("\nFrontend dependencies (node_modules) missing.")
        print("Installing frontend dependencies... This may take a minute.")
        try:
            # Use cmd /c for Windows to bypass PowerShell script execution policies
            command = "cmd /c npm install" if os.name == 'nt' else "npm install"
            subprocess.run(command, cwd=frontend_path, shell=True, check=True)
            print("Frontend dependencies installed successfully.\n")
        except subprocess.CalledProcessError:
            print("Error: Failed to install frontend dependencies. Please run 'npm install' manually in the frontend folder.")
            sys.exit(1)

    # 2. Check Backend (FastAPI check as a proxy for requirements)
    try:
        import fastapi
    except ImportError:
        print("\nBackend dependencies missing.")
        print("Installing backend dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
            print("Backend dependencies installed successfully.\n")
        except subprocess.CalledProcessError:
            print("Error: Failed to install backend dependencies. Please run 'pip install -r backend/requirements.txt' manually.")
            sys.exit(1)

def check_models():
    """Check if recommendation models are trained."""
    models_dir = os.path.join(root, "backend", "app", "models")
    indicator_file = os.path.join(models_dir, "cf_model.pkl")
    
    if not os.path.exists(indicator_file):
        print("\n" + "!" * 50)
        print("WARNING: AI Recommendation models not found!")
        print("The application will run, but recommendations will be empty.")
        print("!" * 50)
        
        choice = input("\nWould you like to train the models now? (y/N): ").lower()
        if choice == 'y':
            print("\nStarting model training... This may take a few minutes.")
            try:
                subprocess.run([sys.executable, "app/train_models.py"], cwd=os.path.join(root, "backend"), check=True)
                print("\nModels trained successfully!\n")
            except subprocess.CalledProcessError:
                print("\nError: Model training failed. You can try running 'python app/train_models.py' manually in the backend folder.\n")
        else:
            print("\nSkipping model training. You can train them later using 'python app/train_models.py' in the backend folder.\n")

print("Checking environment and dependencies...")
check_dependencies()
check_models()

print("-" * 50)
print("Starting BookSage-AI...")
print("-" * 50)

# Start backend and frontend
backend = subprocess.Popen([sys.executable, "run.py", "--prod"], cwd=f"{root}/backend", shell=True)
frontend_command = "cmd /c npm run dev" if os.name == 'nt' else ["npm", "run", "dev"]
frontend = subprocess.Popen(frontend_command, cwd=f"{root}/frontend", shell=True)

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
