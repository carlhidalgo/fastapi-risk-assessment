from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Create engine
engine = create_engine(
    str(settings.DATABASE_URL),
    echo=settings.ENVIRONMENT == "development",  # Log SQL queries in development
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


# Dependency to get database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
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
