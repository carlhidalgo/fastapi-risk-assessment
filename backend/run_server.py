#!/usr/bin/env python3
import os
import sys

# Change to the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Add the backend directory to the Python path
sys.path.insert(0, backend_dir)

# Now import and run the app
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
