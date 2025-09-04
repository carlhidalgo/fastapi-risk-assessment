import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


class TestAuth:
    """Test authentication endpoints"""

    def test_register_user(self, client: TestClient, test_user_data):
        """Test user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json=test_user_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_existing_user(self, client: TestClient, test_user_db, test_user_data):
        """Test registration with existing email"""
        response = client.post(
            "/api/v1/auth/register",
            json=test_user_data
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email"""
        invalid_data = {
            "email": "invalid-email",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        response = client.post(
            "/api/v1/auth/register",
            json=invalid_data
        )
        assert response.status_code == 422

    def test_login_success(self, client: TestClient, test_user_db, test_user_data):
        """Test successful login"""
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_email(self, client: TestClient, test_user_db):
        """Test login with wrong email"""
        login_data = {
            "email": "wrong@example.com",
            "password": "testpassword123"
        }
        response = client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_login_wrong_password(self, client: TestClient, test_user_db, test_user_data):
        """Test login with wrong password"""
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post(
            "/api/v1/auth/login",
            json=login_data
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]

    def test_get_current_user(self, client: TestClient, test_user_db, auth_headers):
        """Test getting current user info"""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_db.email
        assert data["full_name"] == test_user_db.full_name
        assert data["id"] == str(test_user_db.id)

    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get(
            "/api/v1/auth/me",
            headers=headers
        )
        assert response.status_code == 401

    def test_get_current_user_no_token(self, client: TestClient):
        """Test getting current user without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403

    # @pytest.mark.asyncio
    # async def test_auth_flow_async(self, async_client: AsyncClient, test_user_data):
    #     """Test complete authentication flow asynchronously"""
    #     # Register
    #     response = await async_client.post(
    #         "/api/v1/auth/register",
    #         json=test_user_data
    #     )
    #     assert response.status_code == 200
    #     
    #     # Login
    #     login_data = {
    #         "email": test_user_data["email"],
    #         "password": test_user_data["password"]
    #     }
    #     response = await async_client.post(
    #         "/api/v1/auth/login",
    #         json=login_data
    #     )
    #     assert response.status_code == 200
    #     token_data = response.json()
    #     
    #     # Get user info
    #     headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    #     response = await async_client.get(
    #         "/api/v1/auth/me",
    #         headers=headers
    #     )
    #     assert response.status_code == 200
    #     user_data = response.json()
    #     assert user_data["email"] == test_user_data["email"]
