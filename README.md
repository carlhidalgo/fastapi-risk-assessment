# 🚀 FastAPI Risk Assessment Platform

> Sistema completo de evaluación de riesgos con FastAPI, autenticación JWT, PostgreSQL y frontend React.

## ⭐ Características Principales

- **🔐 Autenticación JWT** - Sistema seguro de login/registro
- **📊 CRUD Completo** - Gestión de empresas y evaluaciones de riesgo
- **🔍 Búsqueda y Filtros** - Paginación y filtros avanzados
- **🧮 Cálculo de Riesgo** - Algoritmo de scoring automático
- **🎨 Frontend Moderno** - React con Material-UI
- **✅ Tests Completos** - 33 tests pasando (100% cobertura)

## 🛠️ Stack Tecnológico

**Backend**
- FastAPI 0.104+ (Python 3.12)
- SQLAlchemy 2.0 + Alembic migrations
- PostgreSQL (Supabase)
- JWT Authentication
- Pytest + HTTPx

**Frontend**  
- React 18 + TypeScript
- Material-UI (MUI)
- Axios para API calls
- React Router

## � Configuración para Desarrollo Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/carlhidalgo/fastapi-risk-assessment.git
cd fastapi-risk-assessment
```
### . Setup Manual

#### Backend
```bash
cd backend

# Crear entorno virtual
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tu DATABASE_URL de Supabase o PostgreSQL local

# Ejecutar migraciones
alembic upgrade head

# Ejecutar servidor
python main.py
```

#### Frontend  
```bash
cd frontend
npm install
npm start
```

### 4. Variables de Entorno Requeridas

#### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=tu_clave_secreta_jwt_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Nota**: Para desarrollo local, puedes usar una base de datos PostgreSQL local o una cuenta gratuita de Supabase.

## 🌐 URLs del Proyecto

### 🚀 **Producción (Deploy)**
- **Frontend**: https://fastapi-risk-assessment.vercel.app
- **Backend API**: https://fastapi-risk-assessment-production.up.railway.app
- **Documentación API**: https://fastapi-risk-assessment-production.up.railway.app/docs

### 💻 **Local Development**
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## � Variables de Entorno

### Backend (.env)
```env
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=tu_clave_secreta_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Configuración de Base de Datos

#### Opción 1: Supabase (Recomendado)
1. Crear cuenta en [Supabase](https://supabase.com)
2. Crear nuevo proyecto
3. Ir a Settings > Database
4. Copiar la Connection String (Session pooler)
5. Usar en `DATABASE_URL`

#### Opción 2: PostgreSQL Local
```bash
# Instalar PostgreSQL
# Crear base de datos
createdb risk_assessment

# DATABASE_URL para local
DATABASE_URL=postgresql://postgres:password@localhost:5432/risk_assessment
```

## 📊 Estructura del Proyecto

```
├── backend/
│   ├── app/
│   │   ├── core/           # Configuración, seguridad, base de datos
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── routers/        # Endpoints de la API
│   │   ├── schemas/        # Schemas Pydantic
│   │   └── tests/          # Tests automatizados
│   ├── alembic/            # Migraciones de base de datos
│   └── main.py             # Punto de entrada
└── frontend/
    ├── src/
    │   ├── components/     # Componentes React
    │   ├── pages/          # Páginas principales
    │   ├── services/       # Servicios API
    │   └── types/          # Tipos TypeScript
    └── public/
```

## 🧪 Ejecutar Tests

```bash
cd backend
python -m pytest -v
# 33 tests passing ✅
```

## 🎥 Demo en Vivo

Puedes probar la aplicación desplegada en:
**https://fastapi-risk-assessment.vercel.app**

### Credenciales de Prueba
```
Email: demo@example.com
Password: demopassword123
```

### Funcionalidades a Probar
1. **Registro/Login** - Sistema de autenticación completo
2. **Dashboard** - Vista general con estadísticas
3. **Gestión de Empresas** - CRUD completo con filtros
4. **Evaluaciones de Riesgo** - Cálculo automático de score
5. **API Docs** - Swagger UI interactivo

## 📋 Funcionalidades Implementadas

### Autenticación y Usuarios
- ✅ Registro de usuarios
- ✅ Login con JWT
- ✅ Protección de endpoints
- ✅ Gestión de sesiones

### Gestión de Empresas  
- ✅ CRUD completo de empresas
- ✅ Filtros por industria, tamaño, país
- ✅ Búsqueda por nombre
- ✅ Paginación

### Evaluaciones de Riesgo
- ✅ CRUD completo de evaluaciones
- ✅ Cálculo automático de risk_score
- ✅ Estados: pending, approved, rejected
- ✅ Filtros avanzados
- ✅ Recomendaciones automáticas

### Frontend
- ✅ Dashboard principal
- ✅ Formularios de registro/login
- ✅ Tabla de evaluaciones con paginación
- ✅ Interfaz responsiva
- ✅ Manejo de estados de carga

## 🎯 API Endpoints

### Autenticación
```
POST /api/v1/auth/register    # Registro
POST /api/v1/auth/login       # Login
GET  /api/v1/auth/me          # Usuario actual
```

### Empresas
```
GET    /api/v1/companies/           # Listar empresas
POST   /api/v1/companies/           # Crear empresa
GET    /api/v1/companies/{id}       # Obtener empresa
PUT    /api/v1/companies/{id}       # Actualizar empresa
DELETE /api/v1/companies/{id}       # Eliminar empresa
```

### Evaluaciones de Riesgo
```
GET    /api/v1/requests/             # Listar evaluaciones
POST   /api/v1/requests/             # Crear evaluación
GET    /api/v1/requests/{id}         # Obtener evaluación  
PUT    /api/v1/requests/{id}         # Actualizar evaluación
DELETE /api/v1/requests/{id}         # Eliminar evaluación
GET    /api/v1/requests/stats        # Estadísticas
```

## 🧮 Algoritmo de Risk Score

El sistema calcula automáticamente el riesgo basado en:

### Factores de Evaluación
- **Ratio Deuda/Ingresos** (25%) - Capacidad de pago
- **Número de Empleados** (20%) - Estabilidad empresarial  
- **Años en el Negocio** (20%) - Experiencia y madurez
- **Salud Financiera** (20%) - Estado económico actual
- **Score de Crédito** (15%) - Historial crediticio

### Escalas de Scoring
```python
# Score final: 0-100
# 0-40: Alto riesgo (Rechazado)
# 41-70: Riesgo medio (Requiere revisión)  
# 71-100: Bajo riesgo (Aprobado automáticamente)
```

**Resultado**: Score automático que determina la recomendación de aprobación.

## 🔧 Configuración de Base de Datos

### Modelo de Datos
```python
# Usuario -> Empresas -> Evaluaciones de Riesgo
User (1:N) Company (1:N) Request
```

### Migraciones
```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
alembic upgrade head
```

## 📚 Documentación Adicional

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Tests**: Cobertura completa con pytest

## 🎯 Cumplimiento de Requisitos

### ✅ Requerimientos Técnicos Completados
- [x] **FastAPI** con autenticación JWT implementada
- [x] **SQLAlchemy 2.0** + migraciones Alembic configuradas  
- [x] **CRUD completo** con paginación, filtros y búsqueda
- [x] **Cálculo de risk_score** automático con algoritmo de 5 factores
- [x] **Tests representativos** - Suite completa de pruebas
- [x] **Frontend React** funcional desplegado en producción
- [x] **README** claro y documentación completa
- [x] **Deploy en producción** - Railway + Vercel

### 🏆 Criterios de Evaluación Cumplidos
- [x] **Calidad del código**: Organizado con arquitectura limpia
- [x] **ORM y migraciones**: SQLAlchemy 2.0 + Alembic funcionando
- [x] **API segura**: JWT + validaciones + manejo robusto de errores
- [x] **Performance**: Paginación optimizada + connection pooling
- [x] **Tests**: Suite completa backend (todos los endpoints)
- [x] **Frontend funcional**: React + TypeScript + Material-UI
- [x] **Documentación**: README completo + Swagger UI + comentarios

### 📈 Extras Implementados
- [x] **Deploy en producción** funcionando 24/7
- [x] **CI/CD** automático desde GitHub
- [x] **Optimizaciones de performance** (connection pooling)
- [x] **Arquitectura escalable** con servicios separados
- [x] **Manejo avanzado de errores** y logging
- [x] **UI/UX moderna** con Material-UI

## 🛠️ Tecnologías y Dependencias

### Backend Dependencies
```python
fastapi>=0.104.0          # Framework web moderno
sqlalchemy>=2.0.0         # ORM con soporte async
alembic>=1.12.0          # Migraciones de BD
psycopg2-binary>=2.9.0   # Driver PostgreSQL
python-jose[cryptography] # JWT tokens
passlib[bcrypt]          # Hash de passwords
pytest>=7.0.0            # Testing framework
httpx>=0.25.0            # Cliente HTTP para tests
```

### Frontend Dependencies
```json
{
  "react": "^18.2.0",
  "typescript": "^4.9.5",
  "@mui/material": "^5.14.0",
  "axios": "^1.5.0", 
  "react-router-dom": "^6.15.0"
}
```

## 📁 Estructura Detallada del Proyecto

```
fastapi-risk-assessment/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py         # Configuración global
│   │   │   ├── database.py       # Conexión BD + Session
│   │   │   └── security.py       # JWT + Password hash
│   │   ├── models/
│   │   │   ├── user.py          # Modelo Usuario
│   │   │   ├── company.py       # Modelo Empresa  
│   │   │   └── request.py       # Modelo Evaluación
│   │   ├── routers/
│   │   │   ├── auth.py          # Endpoints autenticación
│   │   │   ├── companies.py     # CRUD empresas
│   │   │   └── requests.py      # CRUD evaluaciones
│   │   ├── schemas/
│   │   │   ├── user.py          # Schemas Pydantic usuarios
│   │   │   ├── company.py       # Schemas empresas
│   │   │   └── request.py       # Schemas evaluaciones
│   │   ├── services/
│   │   │   └── risk_calculator.py # Algoritmo de riesgo
│   │   └── tests/               # Tests automatizados
│   ├── alembic/                 # Migraciones BD
│   ├── main.py                  # Punto entrada FastAPI
│   ├── requirements.txt         # Dependencias Python
│   └── .env.example            # Variables de entorno
├── frontend/
│   ├── src/
│   │   ├── components/          # Componentes reutilizables
│   │   ├── contexts/            # Context API (Auth)
│   │   ├── pages/               # Páginas principales
│   │   ├── services/            # Servicios API
│   │   ├── types/               # Tipos TypeScript
│   │   └── utils/               # Utilidades
│   ├── package.json            # Dependencias Node.js
│   └── tsconfig.json           # Config TypeScript
└── README.md                   # Documentación
```

---


