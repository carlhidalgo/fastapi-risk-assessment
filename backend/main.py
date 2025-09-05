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

# Middleware para manejar errores de base de datos silenciosamente en Railway
class DatabaseErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # En Railway, solo manejar errores específicos de conexión
            if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"):
                error_message = str(exc).lower()
                # Solo convertir a 503 errores reales de conexión/timeout
                if any(conn_error in error_message for conn_error in 
                       ['connection failed', 'network is unreachable', 'timeout', 
                        'connection refused', 'connection reset', 'pool timeout']):
                    return JSONResponse(
                        status_code=503,
                        content={"detail": "Service temporarily unavailable"}
                    )
            
            # Para otros errores (incluyendo 401, 404, etc.), usar el handler por defecto
            raise exc

# Agregar middleware de errores solo en Railway
if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("RAILWAY_PROJECT_ID"):
    app.add_middleware(DatabaseErrorMiddleware)

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
