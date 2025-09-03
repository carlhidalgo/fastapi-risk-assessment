#!/usr/bin/env python3
"""
Script to create database tables directly using SQLAlchemy
This bypasses Alembic migration issues for initial setup
"""
import sys
import os
import asyncio
from sqlalchemy import create_engine, text

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from app.models.base import Base
from app.models.user import User
from app.models.company import Company
from app.models.request import Request

def create_tables():
    """Create all tables in the database"""
    # Use sync engine for table creation
    database_url = "postgresql://postgres:postgres@localhost:5432/postgres"
    engine = create_engine(database_url, echo=True)
    
    try:
        # Test connection first
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            print(f"✅ Database connection successful: {result.fetchone()[0]}")
        
        # Create all tables
        print("🔨 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # List created tables
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            print("\n📋 Created tables:")
            for table in tables:
                print(f"  - {table[0]}")
                
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)
