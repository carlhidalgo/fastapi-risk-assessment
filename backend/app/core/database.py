from typing import Generator
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings

# Create engine with better error handling
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=settings.ENVIRONMENT == "development",  # Log SQL queries in development
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_timeout=20,   # Timeout after 20 seconds
    max_overflow=10,   # Allow 10 additional connections beyond pool_size
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


# Dependency to get database session with better error handling
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error: {str(e)}")
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
