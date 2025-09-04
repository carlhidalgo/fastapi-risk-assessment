import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


class TestCompanies:
    """Test companies CRUD endpoints"""

    def test_create_company(self, client: TestClient, auth_headers, test_company_data):
        """Test company creation"""
        response = client.post(
            "/api/v1/companies/",
            json=test_company_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_company_data["name"]
        assert data["email"] == test_company_data["email"]
        assert "id" in data
        assert "created_at" in data

    def test_create_company_unauthorized(self, client: TestClient, test_company_data):
        """Test company creation without authentication"""
        response = client.post(
            "/api/v1/companies/",
            json=test_company_data
        )
        assert response.status_code == 403

    def test_get_companies_empty(self, client: TestClient, auth_headers):
        """Test getting companies when none exist"""
        response = client.get(
            "/api/v1/companies/",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_companies_with_data(self, client: TestClient, auth_headers, test_company_data):
        """Test getting companies with existing data"""
        # Create a company first
        create_response = client.post(
            "/api/v1/companies/",
            json=test_company_data,
            headers=auth_headers
        )
        assert create_response.status_code == 200
        
        # Get companies
        response = client.get(
            "/api/v1/companies/",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == test_company_data["name"]

    def test_get_company_by_id(self, client: TestClient, auth_headers, test_company_data):
        """Test getting specific company by ID"""
        # Create a company first
        create_response = client.post(
            "/api/v1/companies/",
            json=test_company_data,
            headers=auth_headers
        )
        company_id = create_response.json()["id"]
        
        # Get company by ID
        response = client.get(
            f"/api/v1/companies/{company_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == company_id
        assert data["name"] == test_company_data["name"]

    def test_get_company_not_found(self, client: TestClient, auth_headers):
        """Test getting non-existent company"""
        response = client.get(
            "/api/v1/companies/999",
            headers=auth_headers
        )
        assert response.status_code == 404

    # NOTE: Company router only has GET and POST endpoints, no PUT/DELETE
    # def test_update_company(self, client: TestClient, auth_headers, test_company_data):
    #     """Test updating company"""
    #     # Create a company first
    #     create_response = client.post(
    #         "/api/v1/companies/",
    #         json=test_company_data,
    #         headers=auth_headers
    #     )
    #     company_id = create_response.json()["id"]
    #     
    #     # Update company
    #     updated_data = test_company_data.copy()
    #     updated_data["name"] = "Updated Company Name"
    #     updated_data["industry"] = "Finance"
    #     
    #     response = client.put(
    #         f"/api/v1/companies/{company_id}",
    #         json=updated_data,
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["name"] == "Updated Company Name"
    #     assert data["industry"] == "Finance"

    # def test_update_company_not_found(self, client: TestClient, auth_headers, test_company_data):
    #     """Test updating non-existent company"""
    #     response = client.put(
    #         "/api/v1/companies/999",
    #         json=test_company_data,
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 404

    # def test_delete_company(self, client: TestClient, auth_headers, test_company_data):
    #     """Test deleting company"""
    #     # Create a company first
    #     create_response = client.post(
    #         "/api/v1/companies/",
    #         json=test_company_data,
    #         headers=auth_headers
    #     )
    #     company_id = create_response.json()["id"]
    #     
    #     # Delete company
    #     response = client.delete(
    #         f"/api/v1/companies/{company_id}",
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["message"] == "Company deleted successfully"
    #     
    #     # Verify company is deleted
    #     get_response = client.get(
    #         f"/api/v1/companies/{company_id}",
    #         headers=auth_headers
    #     )
    #     assert get_response.status_code == 404

    # def test_delete_company_not_found(self, client: TestClient, auth_headers):
    #     """Test deleting non-existent company"""
    #     response = client.delete(
    #         "/api/v1/companies/999",
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 404

    def test_user_isolation(self, client: TestClient, test_user_data, test_company_data):
        """Test that users can only see their own companies"""
        # Create first user and company
        user1_response = client.post("/api/v1/auth/register", json=test_user_data)
        user1_id = user1_response.json()["id"]
        
        login1_response = client.post("/api/v1/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        user1_token = login1_response.json()["access_token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}
        
        company1_response = client.post(
            "/api/v1/companies/",
            json=test_company_data,
            headers=user1_headers
        )
        assert company1_response.status_code == 200
        
        # Create second user
        user2_data = {
            "email": "user2@example.com",
            "password": "password123",
            "full_name": "User Two"
        }
        user2_response = client.post("/api/v1/auth/register", json=user2_data)
        
        login2_response = client.post("/api/v1/auth/login", json={
            "email": user2_data["email"],
            "password": user2_data["password"]
        })
        user2_token = login2_response.json()["access_token"]
        user2_headers = {"Authorization": f"Bearer {user2_token}"}
        
        # User 2 should not see User 1's companies
        companies_response = client.get(
            "/api/v1/companies/",
            headers=user2_headers
        )
        assert companies_response.status_code == 200
        assert companies_response.json() == []

    def test_create_company_invalid_data(self, client: TestClient, auth_headers):
        """Test company creation with invalid data"""
        invalid_data = {
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email
            "annual_revenue": -1000  # Negative revenue
        }
        response = client.post(
            "/api/v1/companies/",
            json=invalid_data,
            headers=auth_headers
        )
        assert response.status_code == 422

    # @pytest.mark.asyncio
    # async def test_companies_crud_async(self, async_client: AsyncClient, auth_headers, test_company_data):
    #     """Test complete CRUD flow asynchronously"""
    #     # Create
    #     response = await async_client.post(
    #         "/api/v1/companies/",
    #         json=test_company_data,
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     company_id = response.json()["id"]
    #     
    #     # Read
    #     response = await async_client.get(
    #         f"/api/v1/companies/{company_id}",
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
