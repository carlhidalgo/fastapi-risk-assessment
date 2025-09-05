import logging
import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configurar logging para Railway
if os.getenv("RAILWAY_ENVIRONMENT"):
    # En Railway, configurar logging mínimo
    logging.basicConfig(
        level=logging.WARNING,
        format='%(levelname)s: %(message)s'
    )
    # Desactivar logs de librerías externas
    logging.getLogger("uvicorn.access").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
else:
    # En desarrollo, logging normal
    logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="FastAPI Risk Assessment",
    description="Risk Assessment API with FastAPI and JWT authentication",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://fastapi-risk-assessment.vercel.app",
        "https://fastapi-risk-assessment-o98p19rwb-carlos-projects-6b913237.vercel.app",
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        logging.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e), "timestamp": datetime.now(timezone.utc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
