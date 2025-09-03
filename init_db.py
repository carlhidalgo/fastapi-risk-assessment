import sys
import os

# Agregar el directorio backend al path
backend_dir = os.path.join(os.path.dirname(__file__), "backend")
sys.path.insert(0, backend_dir)

from app.core.database import engine, Base
from app.models.user import User
from app.models.company import Company

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    os.chdir(backend_dir)
    init_db()
