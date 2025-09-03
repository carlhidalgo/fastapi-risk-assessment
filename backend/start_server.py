import os
import sys
import subprocess

# Ensure we're in the backend directory
backend_dir = r"C:\Users\carlos\OneDrive\Documentos\Prueba_tecnica_fastAPI\backend"
os.chdir(backend_dir)

# Set environment variable for the .env file
os.environ["PYTHONPATH"] = backend_dir

# Use subprocess to run uvicorn with proper environment
try:
    print("Starting FastAPI server on port 8002...")
    print(f"Working directory: {os.getcwd()}")
    
    # Run uvicorn as a subprocess
    result = subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0",
        "--port", "8002",
        "--reload"
    ], cwd=backend_dir, check=False)
    
except KeyboardInterrupt:
    print("\nShutting down server...")
except Exception as e:
    print(f"Error starting server: {e}")
    # Fallback to direct execution
    print("Trying direct execution...")
    try:
        import main
        import uvicorn
        uvicorn.run(main.app, host="0.0.0.0", port=8002)
    except Exception as e2:
        print(f"Fallback also failed: {e2}")
