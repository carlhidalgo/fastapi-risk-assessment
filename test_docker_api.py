#!/usr/bin/env python3

import requests
import json

def test_api_connectivity():
    """Test Docker container API connectivity"""
    
    # Test health endpoint
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test API documentation
    print("\n🔍 Testing API docs...")
    try:
        response = requests.get("http://localhost:8000/docs", timeout=10)
        print(f"✅ API docs: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs failed: {e}")
    
    # Test login endpoint
    print("\n🔍 Testing login endpoint...")
    try:
        login_data = {
            "username": "testuser",
            "password": "testpass"
        }
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data,
            timeout=10
        )
        print(f"✅ Login endpoint: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Login endpoint failed: {e}")
    
    # Test companies endpoint
    print("\n🔍 Testing companies endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/companies/", timeout=10)
        print(f"✅ Companies endpoint: {response.status_code}")
        if response.status_code == 200:
            companies = response.json()
            print(f"   Found {len(companies)} companies")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Companies endpoint failed: {e}")
    
    return True

if __name__ == "__main__":
    print("🚀 Testing Docker API connectivity...\n")
    test_api_connectivity()
    print("\n✨ Test completed!")
