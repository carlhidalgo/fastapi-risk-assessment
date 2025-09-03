#!/usr/bin/env python3
import os
import sys

# Change to the backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Add the backend directory to the Python path
sys.path.insert(0, backend_dir)

# Test environment loading
try:
    from app.core.config import settings
    print(f"Settings loaded successfully:")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"SECRET_KEY: {settings.SECRET_KEY[:10]}...")
    print(f"PROJECT_NAME: {settings.PROJECT_NAME}")
except Exception as e:
    print(f"Error loading settings: {e}")
    import traceback
    traceback.print_exc()

# Test database connection
try:
    from app.core.database import engine
    print("Database engine created successfully")
    
    # Test connection
    with engine.connect() as conn:
        print("Database connection successful")
except Exception as e:
    print(f"Error connecting to database: {e}")
    import traceback
    traceback.print_exc()

# Test app import
try:
    from main import app
    print("FastAPI app imported successfully")
except Exception as e:
    print(f"Error importing app: {e}")
    import traceback
    traceback.print_exc()
