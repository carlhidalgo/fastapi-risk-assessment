import requests
import json

# Test API endpoints
base_url = "http://localhost:8001/api/v1"

def test_register():
    """Test user registration"""
    data = {
        "email": "test_user@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{base_url}/auth/register", json=data)
    print(f"Register Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Response data: {response.json()}")
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

def test_login():
    """Test user login"""
    data = {
        "email": "test_user@example.com",
        "password": "testpassword123"
    }
    
    response = requests.post(f"{base_url}/auth/login", json=data)
    print(f"Login Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Response data: {response.json()}")
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

def test_health():
    """Test health endpoint"""
    response = requests.get("http://localhost:8001/health")
    print(f"Health Response: {response.status_code}")
    if response.status_code == 200:
        print(f"Response data: {response.json()}")
        return response.json()
    else:
        print(f"Error: {response.text}")
        return None

if __name__ == "__main__":
    print("Testing API endpoints...")
    print("\n1. Testing health endpoint:")
    test_health()
    
    print("\n2. Testing register endpoint:")
    test_register()
    
    print("\n3. Testing login endpoint:")
    test_login()
