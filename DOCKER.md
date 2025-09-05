# 🐳 Docker Setup - Risk Assessment FastAPI

Este proyecto está configurado para ejecutarse completamente con Docker, incluyendo backend FastAPI y frontend React, usando Supabase como base de datos.

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker Desktop instalado
- Cuenta en Supabase configurada
- Variables de entorno configuradas

### 1. Configurar Variables de Entorno

Asegúrate de que `backend/.env` contenga:
```bash
# Database Configuration (Supabase)
DATABASE_URL=postgresql://postgres:tu_password@db.tu_proyecto.supabase.co:5432/postgres

# JWT Security
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
```

### 2. Construir y Ejecutar

```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# En modo detached (segundo plano)
docker-compose up -d --build

# Solo rebuilding un servicio específico
docker-compose up --build backend
docker-compose up --build frontend
```

### 3. Acceder a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🛠️ Comandos Útiles

### Gestión de Contenedores
```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir sin cache
docker-compose build --no-cache
```

### Desarrollo
```bash
# Ejecutar comandos dentro de un contenedor
docker-compose exec backend bash
docker-compose exec frontend sh

# Ver estado de los contenedores
docker-compose ps

# Ver uso de recursos
docker stats
```

## 📁 Estructura del Proyecto

```
proyecto/
├── docker-compose.yml          # Orquestación de servicios
├── backend/
│   ├── Dockerfile             # Imagen del backend
│   ├── .env                   # Variables de entorno
│   ├── .dockerignore          # Archivos a ignorar
│   └── ...
└── frontend/
    ├── Dockerfile             # Multi-stage build con nginx
    ├── nginx.conf             # Configuración del servidor web
    ├── .dockerignore          # Archivos a ignorar
    └── ...
```

## 🔧 Configuración Avanzada

### Variables de Entorno en Docker

El `docker-compose.yml` está configurado para:
- Usar el archivo `.env` del backend
- Pasar variables específicas al frontend
- Configurar networking entre servicios

### Health Checks

Ambos servicios tienen health checks configurados:
- **Backend**: `GET /health`
- **Frontend**: Nginx status

### Networking

Los servicios se comunican a través de la red `app-network`:
- El frontend puede acceder al backend en `http://backend:80`
- El backend se conecta a Supabase externamente

## 🐛 Troubleshooting

### Problemas Comunes

1. **Error de conexión a base de datos**
   ```bash
   # Verificar variables de entorno
   docker-compose exec backend env | grep DATABASE_URL
   ```

2. **Frontend no carga**
   ```bash
   # Verificar logs del frontend
   docker-compose logs frontend
   ```

3. **Puertos ocupados**
   ```bash
   # Cambiar puertos en docker-compose.yml
   ports:
     - "8001:80"  # Backend en puerto 8001
     - "3001:80"  # Frontend en puerto 3001
   ```

### Limpieza Completa

```bash
# Eliminar todo (contenedores, redes, imágenes)
docker-compose down -v --rmi all
docker system prune -a
```

## 📊 Monitoreo

### Logs Estructurados
```bash
# Logs con timestamps
docker-compose logs -f -t

# Filtrar logs por nivel
docker-compose logs | grep ERROR
```

### Métricas de Rendimiento
```bash
# Uso de recursos por contenedor
docker stats $(docker-compose ps -q)
```

## 🚀 Despliegue en Producción

Para producción, considera:

1. **Variables de entorno seguras**
2. **Reverse proxy (nginx/traefik)**
3. **SSL/TLS certificates**
4. **Monitoring y logging centralizados**
5. **Backups de configuración**

### Ejemplo de producción:
```bash
# Usar archivo de compose específico para producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
