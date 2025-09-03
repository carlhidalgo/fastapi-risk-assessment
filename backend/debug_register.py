#!/usr/bin/env python3

import sys
sys.path.append(".")

from app.schemas.schemas import UserCreate
from app.core.database import get_db
from sqlalchemy.orm import Session
import main

# Test the registration function directly with more debugging
def test_register_detailed():
    print("Testing registration endpoint with detailed debugging...")
    
    try:
        # Create test data
        user_data = UserCreate(
            name="Test User",
            email="test@example.com", 
            password="testpassword123"
        )
        print(f"User data created: {user_data}")
        
        # Get database session
        db_gen = get_db()
        db = next(db_gen)
        print("Database session obtained")
        
        try:
            # Call the registration function directly
            print("Calling register function...")
            result = main.register(user_data, db)
            print("Registration successful!")
            print(f"User ID: {result.id}")
            print(f"User Email: {result.email}")
            print(f"User Name: {result.name}")
            return True
        except Exception as e:
            print(f"Registration failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_register_detailed()
