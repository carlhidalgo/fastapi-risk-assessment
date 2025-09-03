import os
import sys
import uvicorn

print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print(f"Python path: {sys.path}")

try:
    from main import app
    print("Successfully imported app from main")
    print(f"App object: {app}")
except Exception as e:
    print(f"Error importing app: {e}")
    exit(1)

if __name__ == "__main__":
    print("Starting uvicorn server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
