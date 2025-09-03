from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crear la instancia de FastAPI
app = FastAPI(
    title="FastAPI Prueba Técnica",
    description="API desarrollada con FastAPI, PostgreSQL y Docker",
    version="1.0.0",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint básico de prueba
@app.get("/")
async def root():
    return {
        "message": "¡Bienvenido a la API de FastAPI!",
        "version": "1.0.0",
        "status": "running"
    }

# Endpoint de health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Aquí se añadirán más endpoints según tus necesidades
