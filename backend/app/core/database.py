from typing import Generator
import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError, TimeoutError

from app.core.config import settings

# Create engine with better error handling and connection pooling
engine_kwargs = {
    "echo": settings.ENVIRONMENT == "development",  # Log SQL queries in development
    "pool_pre_ping": True,
    "pool_recycle": 300,  # Recycle connections every 5 minutes
    "pool_timeout": 20,   # Timeout after 20 seconds
    "max_overflow": 10,   # Allow 10 additional connections beyond pool_size
    "pool_size": 5,       # Base pool size
}

# In Railway, add more aggressive timeout settings
if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"):
    engine_kwargs.update({
        "echo": False,  # Never echo in Railway
        "pool_timeout": 5,  # Muy corto timeout
        "pool_recycle": 60,  # Reciclar cada minuto
        "pool_size": 1,      # Solo 1 conexión base
        "max_overflow": 2,   # Máximo 3 conexiones total (1+2)
        "connect_args": {
            "connect_timeout": 5
        }
    })

engine = create_engine(str(settings.DATABASE_URL), **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


# Dependency to get database session with better error handling
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except (SQLAlchemyError, DisconnectionError, TimeoutError) as e:
        db.rollback()
        # Only log in development or for critical errors
        if not (os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID")):
            logging.error(f"Database error: {str(e)}")
        raise
    except Exception as e:
        db.rollback()
        # Suppress connection-related errors in Railway
        if not (os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID")):
            logging.error(f"Unexpected database error: {str(e)}")
        raise
    finally:
        db.close()


# Database utility functions
def init_db() -> None:
    """Initialize database tables"""
    # Import all models here to ensure they are registered with Base
    from app.models import user, company, request  # noqa
    
    # Create all tables
    Base.metadata.create_all(bind=engine)


def close_db() -> None:
    """Close database connections"""
    engine.dispose()
