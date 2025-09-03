#!/usr/bin/env python3
"""
Simple test to verify FastAPI application starts correctly
"""
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_app_import():
    """Test that the FastAPI app can be imported successfully"""
    try:
        from main import app
        print("✅ FastAPI app imported successfully")
        
        # Check routes
        routes = [route.path for route in app.routes]
        print("📋 Available routes:")
        for route in routes:
            print(f"  - {route}")
        
        print(f"\n🏷️  App title: {app.title}")
        print(f"📝 App description: {app.description}")
        print(f"🔢 App version: {app.version}")
        
        return True
    except Exception as e:
        print(f"❌ Error importing app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Test database connection works"""
    try:
        from app.core.database import engine
        print("✅ Database engine created successfully")
        
        # Test basic SQL connection
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            print(f"✅ Database connection test: {result.fetchone()}")
        
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_models():
    """Test that models can be imported"""
    try:
        from app.models.user import User
        from app.models.company import Company
        from app.models.request import Request
        print("✅ All models imported successfully")
        
        print("📋 Model classes:")
        print(f"  - User: {User.__tablename__}")
        print(f"  - Company: {Company.__tablename__}")
        print(f"  - Request: {Request.__tablename__}")
        
        return True
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running FastAPI application tests...")
    print("=" * 50)
    
    all_tests_passed = True
    
    print("\n1️⃣ Testing app import...")
    if not test_app_import():
        all_tests_passed = False
    
    print("\n2️⃣ Testing models...")
    if not test_models():
        all_tests_passed = False
    
    print("\n3️⃣ Testing database connection...")
    if not test_database_connection():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To start the server, run:")
        print("   python -m uvicorn main:app --host 127.0.0.1 --port 8001")
        print("\n📚 Documentation available at:")
        print("   http://127.0.0.1:8001/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    sys.exit(0 if all_tests_passed else 1)
