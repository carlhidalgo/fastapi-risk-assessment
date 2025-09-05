import logging
import os
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# Configurar logging de manera más agresiva para Railway
if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"):
    # En Railway, configurar logging mínimo
    logging.basicConfig(
        level=logging.ERROR,  # Solo errores críticos
        format='%(levelname)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )
    # Desactivar completamente logs de librerías externas
    logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
    logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
    logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)
    logging.getLogger("sqlalchemy").setLevel(logging.CRITICAL)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.CRITICAL)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.CRITICAL)
    logging.getLogger("fastapi").setLevel(logging.ERROR)
    logging.getLogger("starlette").setLevel(logging.ERROR)
    
    # Desactivar el root logger también
    logging.getLogger().setLevel(logging.CRITICAL)
else:
    # En desarrollo, logging normal
    logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="FastAPI Risk Assessment",
    description="Risk Assessment API with FastAPI and JWT authentication",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

# CORS middleware - DEBE IR PRIMERO SIEMPRE
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://fastapi-risk-assessment.vercel.app",
        "https://fastapi-risk-assessment-o98p19rwb-carlos-projects-6b913237.vercel.app",
        "https://*.vercel.app",
        "*"  # Temporal para debugging
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Crear tablas automáticamente al iniciar
@app.on_event("startup")
async def startup_event():
    try:
        from app.core.database import engine, Base
        from app.models import user, company, request  # Import all models
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Health checks primero
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

@app.get("/health/db")
def health_check_db():
    """Database health check endpoint"""
    try:
        from app.core.database import engine
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return {"status": "healthy", "database": "connected", "timestamp": datetime.now(timezone.utc)}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e), "timestamp": datetime.now(timezone.utc)}

# Import and include routers
try:
    from app.routers import auth, companies, risk, requests
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(companies.router, prefix="/api/v1")
    app.include_router(risk.router, prefix="/api/v1")
    app.include_router(requests.router, prefix="/api/v1")
    print("All routers loaded successfully")
except Exception as e:
    print(f"Error loading routers: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
