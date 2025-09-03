# Backend - Risk Assessment API

FastAPI application with SQLAlchemy 2.0, PostgreSQL, and JWT authentication.

## Local Development

### With Docker (Recommended)
```bash
docker-compose up --build
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up database (requires PostgreSQL running)
alembic upgrade head

# Run development server
uvicorn app.main:app --reload --port 8000
```

## API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Testing
```bash
pytest app/tests/ -v --cov=app
```

## Environment Variables
Copy `.env.example` to `.env` and configure:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Project Structure
```
app/
├── main.py              # FastAPI application
├── core/
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   └── security.py      # Authentication utilities
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── api/v1/              # API routes
└── tests/               # Test suite
```
