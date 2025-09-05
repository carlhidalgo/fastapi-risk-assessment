from typing import List
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Risk Assessment"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Risk Assessment API with FastAPI, PostgreSQL, and JWT authentication"
    
    # Security
    SECRET_KEY: str = "tu_clave_secreta_muy_segura_aqui_cambiala_en_produccion_2025"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database - Lee desde variable de entorno, fallback para desarrollo local
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/fastapi_risk_db")
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Debug: Print database URL (sin mostrar credenciales completas)
db_url_masked = settings.DATABASE_URL.replace(settings.DATABASE_URL.split('@')[0].split('//')[1], '***') if '@' in settings.DATABASE_URL else settings.DATABASE_URL
print(f"Database connection URL: {db_url_masked}")
print(f"Environment: {settings.ENVIRONMENT}")
