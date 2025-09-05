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

# Render optimization - much better for PostgreSQL
if os.getenv("RENDER"):
    engine_kwargs.update({
        "echo": False,
        "pool_timeout": 30,  # Generous timeout for Render
        "pool_recycle": 300,  # 5 minutes
        "pool_size": 5,      # Standard pool
        "max_overflow": 10,  # Total 15 connections
        "pool_reset_on_return": "commit"
    })
# Railway optimization (fallback)
elif os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"):
    engine_kwargs.update({
        "echo": False,  # Never echo in Railway
        "pool_timeout": 10,  # Más tiempo para obtener conexión
        "pool_recycle": 60,  # Reciclar cada minuto
        "pool_size": 3,      # 3 conexiones base  
        "max_overflow": 2,   # Máximo 5 conexiones total (3+2)
        "pool_reset_on_return": "commit",  # Reset connections
        "connect_args": {
            "connect_timeout": 10,
            "options": "-c statement_timeout=15000"  # 15 second query timeout
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
