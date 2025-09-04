import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


class TestRequests:
    """Test requests CRUD endpoints with pagination and filtering"""

    def setup_company(self, client: TestClient, auth_headers, test_company_data):
        """Helper method to create a company for testing"""
        response = client.post(
            "/api/v1/companies/",
            json=test_company_data,
            headers=auth_headers
        )
        return response.json()["id"]

    def test_create_request(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test request creation"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        request_data = test_request_data.copy()
        request_data["company_id"] = company_id
        
        response = client.post(
            "/api/v1/requests/",
            json=request_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == test_request_data["amount"]
        assert data["purpose"] == test_request_data["purpose"]
        assert data["company_id"] == company_id
        assert "id" in data
        assert "created_at" in data

    def test_create_request_unauthorized(self, client: TestClient, test_request_data):
        """Test request creation without authentication"""
        response = client.post(
            "/api/v1/requests/",
            json=test_request_data
        )
        assert response.status_code == 403

    def test_create_request_invalid_company(self, client: TestClient, auth_headers, test_request_data):
        """Test request creation with invalid company"""
        request_data = test_request_data.copy()
        request_data["company_id"] = "999"  # Non-existent company as string

        response = client.post(
            "/api/v1/requests/",
            json=request_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_get_requests_empty(self, client: TestClient, auth_headers):
        """Test getting requests when none exist"""
        response = client.get(
            "/api/v1/requests/",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["size"] == 10

    def test_get_requests_with_pagination(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test getting requests with pagination"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        # Create multiple requests
        for i in range(5):
            request_data = test_request_data.copy()
            request_data["company_id"] = company_id
            request_data["purpose"] = f"Purpose {i}"
            request_data["amount"] = 10000 * (i + 1)
            
            response = client.post(
                "/api/v1/requests/",
                json=request_data,
                headers=auth_headers
            )
            assert response.status_code == 200
        
        # Test pagination
        response = client.get(
            "/api/v1/requests/?page=1&size=3",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 3
        assert data["total"] == 5
        assert data["page"] == 1
        assert data["size"] == 3
        assert data["pages"] == 2

    def test_get_requests_with_filters(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test getting requests with various filters"""
        company_id = self.setup_company(client, auth_headers, test_company_data)

        # Create requests with different attributes
        request_configs = [
            {"amount": 10000, "status": "pending"},
            {"amount": 50000, "status": "approved"},
            {"amount": 100000, "status": "rejected"},
        ]

        request_ids = []
        for config in request_configs:
            request_data = test_request_data.copy()
            request_data["company_id"] = company_id
            request_data["amount"] = config["amount"]

            # Create request
            response = client.post(
                "/api/v1/requests/",
                json=request_data,
                headers=auth_headers
            )
            assert response.status_code == 200
            request_id = response.json()["id"]
            request_ids.append(request_id)
            
            # Update status if needed
            if config["status"] != "pending":
                update_data = {"status": config["status"]}
                update_response = client.put(
                    f"/api/v1/requests/{request_id}",
                    json=update_data,
                    headers=auth_headers
                )
                assert update_response.status_code == 200

        # Test status filter
        response = client.get(
            "/api/v1/requests/?status=approved",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["status"] == "approved"

        # Test amount filters
        response = client.get(
            "/api/v1/requests/?min_amount=50000",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) >= 1  # Should include requests >= 50000
        
        # Test amount range filter
        response = client.get(
            "/api/v1/requests/?min_amount=40000&max_amount=60000",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["amount"] == 50000

    def test_get_requests_with_search(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test getting requests with search functionality"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        # Create requests with different purposes
        purposes = ["Equipment financing", "Working capital", "Expansion loan"]
        
        for purpose in purposes:
            request_data = test_request_data.copy()
            request_data["company_id"] = company_id
            request_data["purpose"] = purpose
            
            response = client.post(
                "/api/v1/requests/",
                json=request_data,
                headers=auth_headers
            )
            assert response.status_code == 200
        
        # Test search by purpose
        response = client.get(
            "/api/v1/requests/?search=Equipment",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert "Equipment" in data["items"][0]["purpose"]

    def test_get_request_by_id(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test getting specific request by ID"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        request_data = test_request_data.copy()
        request_data["company_id"] = company_id
        
        create_response = client.post(
            "/api/v1/requests/",
            json=request_data,
            headers=auth_headers
        )
        request_id = create_response.json()["id"]
        
        response = client.get(
            f"/api/v1/requests/{request_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == request_id
        assert data["amount"] == test_request_data["amount"]

    def test_get_request_not_found(self, client: TestClient, auth_headers):
        """Test getting non-existent request"""
        response = client.get(
            "/api/v1/requests/999",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_update_request(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test updating request"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        request_data = test_request_data.copy()
        request_data["company_id"] = company_id
        
        create_response = client.post(
            "/api/v1/requests/",
            json=request_data,
            headers=auth_headers
        )
        request_id = create_response.json()["id"]
        
        # Update request
        updated_data = request_data.copy()
        updated_data["amount"] = 75000.0
        updated_data["status"] = "approved"

        response = client.put(
            f"/api/v1/requests/{request_id}",
            json=updated_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == 75000.0
        assert data["status"] == "approved"

    def test_update_request_not_found(self, client: TestClient, auth_headers, test_request_data):
        """Test updating non-existent request"""
        response = client.put(
            "/api/v1/requests/999",
            json=test_request_data,
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_request(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test deleting request"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        request_data = test_request_data.copy()
        request_data["company_id"] = company_id
        
        create_response = client.post(
            "/api/v1/requests/",
            json=request_data,
            headers=auth_headers
        )
        request_id = create_response.json()["id"]
        
        # Delete request
        response = client.delete(
            f"/api/v1/requests/{request_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Request deleted successfully"
        
        # Verify request is deleted
        get_response = client.get(
            f"/api/v1/requests/{request_id}",
            headers=auth_headers
        )
        assert get_response.status_code == 404

    def test_delete_request_not_found(self, client: TestClient, auth_headers):
        """Test deleting non-existent request"""
        response = client.delete(
            "/api/v1/requests/999",
            headers=auth_headers
        )
        assert response.status_code == 404

    def test_get_requests_statistics(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test getting requests statistics"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        # Create requests with different statuses
        statuses = ["pending", "approved", "rejected"]
        amounts = [10000, 50000, 30000]
        
        request_ids = []
        for status, amount in zip(statuses, amounts):
            request_data = test_request_data.copy()
            request_data["company_id"] = company_id
            request_data["amount"] = amount
            
            # Create request
            response = client.post(
                "/api/v1/requests/",
                json=request_data,
                headers=auth_headers
            )
            assert response.status_code == 200
            request_id = response.json()["id"]
            request_ids.append(request_id)
            
            # Update status if not pending
            if status != "pending":
                update_response = client.put(
                    f"/api/v1/requests/{request_id}",
                    json={"status": status},
                    headers=auth_headers
                )
                assert update_response.status_code == 200
        
        # Get statistics
        response = client.get(
            "/api/v1/requests/stats/summary",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_requests"] == 3
        assert data["total_amount_requested"] == 90000
        assert data["approved_requests"] == 1
        assert data["rejected_requests"] == 1
        assert data["pending_requests"] == 1

    def test_user_isolation_requests(self, client: TestClient, test_user_data, test_company_data, test_request_data):
        """Test that users can only see their own requests"""
        # Create first user, company, and request
        user1_response = client.post("/api/v1/auth/register", json=test_user_data)
        
        login1_response = client.post("/api/v1/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        user1_token = login1_response.json()["access_token"]
        user1_headers = {"Authorization": f"Bearer {user1_token}"}
        
        company1_id = self.setup_company(client, user1_headers, test_company_data)
        
        request_data = test_request_data.copy()
        request_data["company_id"] = company1_id
        
        request1_response = client.post(
            "/api/v1/requests/",
            json=request_data,
            headers=user1_headers
        )
        assert request1_response.status_code == 200
        
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
        
        # User 2 should not see User 1's requests
        requests_response = client.get(
            "/api/v1/requests/",
            headers=user2_headers
        )
        assert requests_response.status_code == 200
        data = requests_response.json()
        assert data["items"] == []
        assert data["total"] == 0

    # @pytest.mark.asyncio
    # async def test_requests_crud_async(self, async_client: AsyncClient, auth_headers, test_company_data, test_request_data):
    #     """Test complete requests CRUD flow asynchronously"""
    #     # Setup company
    #     company_response = await async_client.post(
    #         "/api/v1/companies/",
    #         json=test_company_data,
    #         headers=auth_headers
    #     )
    #     company_id = company_response.json()["id"]
    #     
    #     request_data = test_request_data.copy()
    #     request_data["company_id"] = company_id
    #     
    #     # Create
    #     response = await async_client.post(
    #         "/api/v1/requests/",
    #         json=request_data,
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     request_id = response.json()["id"]
    #     
    #     # Read
    #     response = await async_client.get(
    #         f"/api/v1/requests/{request_id}",
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     
    #     # Update
    #     updated_data = request_data.copy()
    #     updated_data["amount"] = 100000.0
    #     updated_data["status"] = "approved"
    #     response = await async_client.put(
    #         f"/api/v1/requests/{request_id}",
    #         json=updated_data,
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["amount"] == 100000.0
    #     assert response.json()["status"] == "approved"
    #     
    #     # Delete
    #     response = await async_client.delete(
    #         f"/api/v1/requests/{request_id}",
    #         headers=auth_headers
    #     )
    #     assert response.status_code == 200

    def test_requests_advanced_filtering_combinations(self, client: TestClient, auth_headers, test_company_data, test_request_data):
        """Test advanced filtering combinations"""
        company_id = self.setup_company(client, auth_headers, test_company_data)
        
        # Create diverse requests with different amounts for filtering
        request_configs = [
            {"amount": 25000, "purpose": "Equipment purchase"},
            {"amount": 75000, "purpose": "Working capital"},
            {"amount": 150000, "purpose": "Business expansion"},
            {"amount": 35000, "purpose": "Equipment upgrade"},
        ]
        
        for config in request_configs:
            request_data = test_request_data.copy()
            request_data["company_id"] = company_id
            request_data["amount"] = config["amount"]
            request_data["purpose"] = config["purpose"]
            
            response = client.post(
                "/api/v1/requests/",
                json=request_data,
                headers=auth_headers
            )
            assert response.status_code == 200
        
        # Test amount filter
        response = client.get(
            "/api/v1/requests/?min_amount=50000",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2  # 75000 and 150000
        
        # Test max amount filter
        response = client.get(
            "/api/v1/requests/?max_amount=50000",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2  # 25000 and 35000
        
        # Test combined filters: amount range + search
        response = client.get(
            "/api/v1/requests/?min_amount=30000&max_amount=80000&search=capital",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["amount"] == 75000
        
        # Test pagination with filters
        response = client.get(
            "/api/v1/requests/?status=pending&page=1&size=1",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["total"] == 4  # All requests are pending by default
        assert data["pages"] == 4  # 4 pages with size 1
