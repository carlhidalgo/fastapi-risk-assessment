from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Risk Assessment"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Risk Assessment API with FastAPI, PostgreSQL, and JWT authentication"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
