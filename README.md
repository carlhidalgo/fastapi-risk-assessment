# Risk Assessment API

> FastAPI application with JWT authentication, PostgreSQL database, and React frontend for risk assessment management.

## 🏗️ Architecture

- **Backend**: FastAPI + SQLAlchemy 2.0 + PostgreSQL (Azure-ready)
- **Frontend**: React (Vercel-ready)
- **Database**: PostgreSQL with Docker
- **Authentication**: JWT tokens

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.12+

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd risk-assessment-api

# Start backend with database
cd backend
docker-compose up --build
```

**API will be available at**: http://localhost:8000/docs

## 📋 Current Status

### ✅ Completed
- [x] Project structure (monorepo)
- [x] Docker configuration
- [x] Basic FastAPI setup
- [x] PostgreSQL integration
- [x] CI/CD workflows

### 🔄 In Progress
- [ ] Database models (User, Company, Request)
- [ ] JWT authentication
- [ ] CRUD operations
- [ ] Risk score calculation
- [ ] React frontend
- [ ] Testing suite

## 🛠️ Tech Stack

**Backend**: FastAPI • SQLAlchemy 2.0 • PostgreSQL • Docker • JWT  
**Frontend**: React • TypeScript • Axios  
**Deploy**: Azure Container Instances • Vercel  
**CI/CD**: GitHub Actions
