import pytest
import asyncio
import sys
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Add backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from app.core.database import get_db
from app.models.base import Base
from main import app
from app.core.security import create_access_token, get_password_hash
from app.models.user import User
from app.models.company import Company
from app.models.request import Request


# Test database URL (SQLite in memory for tests)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create test database session"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with database override"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client():
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }


@pytest.fixture
def test_user_db(db_session, test_user_data):
    """Create test user in database"""
    user = User(
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        full_name=test_user_data["full_name"],
        is_active=True,
        is_superuser=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user_db):
    """Create authentication headers for test user"""
    access_token = create_access_token(
        subject=str(test_user_db.id)
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_company_data():
    """Test company data"""
    return {
        "name": "Test Company",
        "email": "company@test.com",
        "phone": "+1234567890",
        "industry": "Technology",
        "annual_revenue": 1000000.0,
        "company_size": 50
    }


@pytest.fixture
def test_request_data():
    """Test request data"""
    return {
        "amount": 50000.0,
        "purpose": "Equipment financing",
        "risk_inputs": {
            "annual_revenue": 1000000.0,
            "employee_count": 50,
            "years_in_business": 5,
            "debt_to_equity_ratio": 0.3,
            "credit_score": 750
        }
    }
