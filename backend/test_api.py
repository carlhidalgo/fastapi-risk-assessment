#!/usr/bin/env python3
"""
Test script for the FastAPI Risk Assessment API
"""
import asyncio
import httpx
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8001"

async def test_api():
    """Test all API endpoints"""
    async with httpx.AsyncClient() as client:
        
        # Test 1: Root endpoint
        print("🧪 Testing root endpoint...")
        response = await client.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Test 2: Health check
        print("🧪 Testing health check...")
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Test 3: Register a new user
        print("🧪 Testing user registration...")
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = await client.post(f"{BASE_URL}/api/v1/auth/register", json=user_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
        
        # Test 4: Login
        print("🧪 Testing user login...")
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = await client.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Status: {response.status_code}")
        login_response = response.json()
        print(f"Response: {login_response}")
        
        if response.status_code == 200:
            token = login_response["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # Test 5: Get current user
            print("\n🧪 Testing get current user...")
            response = await client.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.json()}")
            print()
            
            # Test 6: Create a company
            print("🧪 Testing create company...")
            company_data = {
                "name": "Test Company Inc.",
                "industry": "Technology",
                "company_size": "50-100"
            }
            response = await client.post(f"{BASE_URL}/api/v1/companies", json=company_data, headers=headers)
            print(f"Status: {response.status_code}")
            company_response = response.json()
            print(f"Response: {company_response}")
            
            if response.status_code == 200:
                company_id = company_response["id"]
                
                # Test 7: Get companies
                print("\n🧪 Testing get companies...")
                response = await client.get(f"{BASE_URL}/api/v1/companies", headers=headers)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
                print()
                
                # Test 8: Create risk assessment
                print("🧪 Testing create risk assessment...")
                risk_data = {
                    "company_id": company_id,
                    "risk_inputs": {
                        "annual_revenue": 250000,
                        "employee_count": 75,
                        "market_volatility": "medium",
                        "technology_adoption": "high"
                    }
                }
                response = await client.post(f"{BASE_URL}/api/v1/risk-assessment", json=risk_data, headers=headers)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
                print()
                
                # Test 9: Get risk assessments
                print("🧪 Testing get risk assessments...")
                response = await client.get(f"{BASE_URL}/api/v1/risk-assessments", headers=headers)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.json()}")
                print()
            
            print("✅ All tests completed!")
        else:
            print("❌ Login failed, skipping authenticated tests")

if __name__ == "__main__":
    print("🚀 Starting API tests...")
    print("Make sure the API server is running on http://localhost:8001")
    print("=" * 50)
    
    try:
        asyncio.run(test_api())
    except Exception as e:
        print(f"❌ Test failed: {e}")
