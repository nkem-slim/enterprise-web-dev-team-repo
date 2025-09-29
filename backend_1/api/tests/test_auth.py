#!/usr/bin/env python3
"""
Test script for authentication functionality
"""

import requests
import base64
import json

def create_auth_header(username, password):
    """Create Basic Auth header"""
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded_credentials}"

def test_authentication():
    """Test authentication functionality"""
    base_url = "http://localhost:8000"
    
    print("Testing Authentication")
    print("=" * 40)
    
    # Test 1: Access without authentication
    print("\n1. Testing without authentication...")
    try:
        response = requests.get(f"{base_url}/transactions")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   Authentication required (expected)")
        else:
            print("   Should require authentication")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Access with valid credentials
    print("\n2. Testing with valid credentials...")
    try:
        headers = {"Authorization": create_auth_header("admin", "admin123")}
        response = requests.get(f"{base_url}/transactions", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success! Found {len(data)} transactions")
        else:
            print(f"   Failed: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Access with invalid credentials
    print("\n3. Testing with invalid credentials...")
    try:
        headers = {"Authorization": create_auth_header("admin", "wrongpassword")}
        response = requests.get(f"{base_url}/transactions", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   Invalid credentials rejected (expected)")
        else:
            print("   Should reject invalid credentials")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Test different users
    print("\n4. Testing different users...")
    users = [
        ("user", "user123"),
        ("test", "test123"),
        ("admin", "admin123")
    ]
    
    for username, password in users:
        try:
            headers = {"Authorization": create_auth_header(username, password)}
            response = requests.get(f"{base_url}/transactions", headers=headers)
            print(f"   {username}: {response.status_code} {'PASS' if response.status_code == 200 else 'FAIL'}")
        except Exception as e:
            print(f"   {username}: Error: {e}")
    
    # Test 5: Test user management (admin only)
    print("\n5. Testing user management...")
    try:
        # Try as regular user
        headers = {"Authorization": create_auth_header("user", "user123")}
        response = requests.get(f"{base_url}/users", headers=headers)
        print(f"   Regular user accessing /users: {response.status_code}")
        if response.status_code == 403:
            print("   Regular user correctly denied access")
        
        # Try as admin
        headers = {"Authorization": create_auth_header("admin", "admin123")}
        response = requests.get(f"{base_url}/users", headers=headers)
        print(f"   Admin accessing /users: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Admin can see {len(data)} users")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Create new user (admin only)
    print("\n6. Testing user creation...")
    try:
        headers = {
            "Authorization": create_auth_header("admin", "admin123"),
            "Content-Type": "application/json"
        }
        new_user = {
            "username": "newuser",
            "password": "newpass123",
            "role": "user"
        }
        response = requests.post(f"{base_url}/users", headers=headers, json=new_user)
        print(f"   Create user status: {response.status_code}")
        if response.status_code == 201:
            print("   User created successfully")
        else:
            print(f"   Failed: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

def show_usage_examples():
    """Show usage examples"""
    print("\nUsage Examples")
    print("=" * 40)
    
    print("\nAuthentication Methods:")
    print("1. Using curl:")
    print("   curl -u admin:admin123 http://localhost:8000/transactions")
    print("   curl -H 'Authorization: Basic YWRtaW46YWRtaW4xMjM=' http://localhost:8000/transactions")
    
    print("\n2. Using Python requests:")
    print("   import requests")
    print("   response = requests.get('http://localhost:8000/transactions', auth=('admin', 'admin123'))")
    
    print("\n3. Using JavaScript fetch:")
    print("   fetch('http://localhost:8000/transactions', {")
    print("     headers: { 'Authorization': 'Basic ' + btoa('admin:admin123') }")
    print("   })")
    
    print("\nDefault Users:")
    print("   admin:admin123 (admin role)")
    print("   user:user123 (user role)")
    print("   test:test123 (user role)")

if __name__ == "__main__":
    test_authentication()
    show_usage_examples()
