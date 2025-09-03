#!/usr/bin/env python3

import sys
sys.path.append(".")

from app.schemas.schemas import UserCreate
from app.core.database import get_db
from sqlalchemy.orm import Session
import main

# Test the registration function directly
def test_register():
    print("Testing registration endpoint...")
    
    # Create test data
    user_data = UserCreate(
        name="Test User",
        email="test@example.com", 
        password="testpassword123"
    )
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Call the registration function directly
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

if __name__ == "__main__":
    test_register()
