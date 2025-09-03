from sqlalchemy import create_engine
from app.models.base import Base
from app.core.config import settings

# Create SQLite database
engine = create_engine(str(settings.DATABASE_URL), echo=True)

# Create all tables
print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
