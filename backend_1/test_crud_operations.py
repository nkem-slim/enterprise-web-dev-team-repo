#!/usr/bin/env python3
"""
Comprehensive test for CRUD operations
"""

import sys
import os
import json
import requests
import base64
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_auth_header(username, password):
    """Create Basic Auth header"""
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded_credentials}"

def test_crud_operations():
    """Test all CRUD operations"""
    base_url = "http://localhost:8000"
    
    print("Testing CRUD Operations")
    print("=" * 50)
    
    # Test data
    test_transaction = {
        "sender_name": "Test Sender",
        "receiver_name": "Test Receiver", 
        "amount": 100.50,
        "fee": 2.50,
        "balance_after": 500.00,
        "transaction_type": "Transfer",
        "status": "Completed",
        "remarks": "Test transaction for CRUD testing"
    }
    
    headers = {"Authorization": create_auth_header("admin", "admin123")}
    
    try:
        # Test 1: CREATE (POST)
        print("\n1. Testing CREATE (POST /transactions)...")
        response = requests.post(f"{base_url}/transactions", 
                               headers=headers, 
                               json=test_transaction)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            created_txn = response.json()
            transaction_id = created_txn['transaction_id']
            print(f"   Transaction created successfully")
            print(f"   ID: {transaction_id}")
        else:
            print(f"   CREATE failed: {response.text}")
            return False
        
        # Test 2: READ (GET specific)
        print(f"\n2. Testing READ (GET /transactions/{transaction_id})...")
        response = requests.get(f"{base_url}/transactions/{transaction_id}", 
                              headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            retrieved_txn = response.json()
            print(f"   Transaction retrieved successfully")
            print(f"   Amount: {retrieved_txn['amount']}")
        else:
            print(f"   READ failed: {response.text}")
            return False
        
        # Test 3: READ ALL (GET all)
        print(f"\n3. Testing READ ALL (GET /transactions)...")
        response = requests.get(f"{base_url}/transactions", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            all_transactions = response.json()
            print(f"   Retrieved {len(all_transactions)} transactions")
        else:
            print(f"   READ ALL failed: {response.text}")
            return False
        
        # Test 4: UPDATE (PUT)
        print(f"\n4. Testing UPDATE (PUT /transactions/{transaction_id})...")
        update_data = {
            "amount": 150.75,
            "remarks": "Updated test transaction",
            "status": "Pending"
        }
        response = requests.put(f"{base_url}/transactions/{transaction_id}", 
                              headers=headers, 
                              json=update_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            updated_txn = response.json()
            print(f"   Transaction updated successfully")
            print(f"   New amount: {updated_txn['amount']}")
            print(f"   New status: {updated_txn['status']}")
        else:
            print(f"   UPDATE failed: {response.text}")
            return False
        
        # Test 5: DELETE
        print(f"\n5. Testing DELETE (DELETE /transactions/{transaction_id})...")
        response = requests.delete(f"{base_url}/transactions/{transaction_id}", 
                                 headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   Transaction deleted successfully")
        else:
            print(f"   DELETE failed: {response.text}")
            return False
        
        # Test 6: Verify deletion
        print(f"\n6. Verifying deletion (GET /transactions/{transaction_id})...")
        response = requests.get(f"{base_url}/transactions/{transaction_id}", 
                              headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 404:
            print(f"   Transaction successfully deleted (404 as expected)")
        else:
            print(f"   Transaction still exists after deletion")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   Connection error - Is the server running?")
        return False
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_authentication():
    """Test authentication requirements"""
    base_url = "http://localhost:8000"
    
    print("\nTesting Authentication")
    print("=" * 30)
    
    # Test without auth
    print("1. Testing without authentication...")
    try:
        response = requests.get(f"{base_url}/transactions")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   Authentication required (expected)")
        else:
            print("   Should require authentication")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test with invalid auth
    print("2. Testing with invalid credentials...")
    try:
        headers = {"Authorization": create_auth_header("admin", "wrongpassword")}
        response = requests.get(f"{base_url}/transactions", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   Invalid credentials rejected")
        else:
            print("   Should reject invalid credentials")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test with valid auth
    print("3. Testing with valid credentials...")
    try:
        headers = {"Authorization": create_auth_header("admin", "admin123")}
        response = requests.get(f"{base_url}/transactions", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Valid credentials accepted")
        else:
            print("   Should accept valid credentials")
    except Exception as e:
        print(f"   Error: {e}")

def test_user_management():
    """Test user management operations"""
    base_url = "http://localhost:8000"
    
    print("\nTesting User Management")
    print("=" * 30)
    
    headers = {"Authorization": create_auth_header("admin", "admin123")}
    
    # Test list users
    print("1. Testing list users...")
    try:
        response = requests.get(f"{base_url}/users", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"   Retrieved {len(users)} users")
        else:
            print(f"   Failed: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test create user
    print("2. Testing create user...")
    try:
        new_user = {
            "username": "testuser",
            "password": "testpass123",
            "role": "user"
        }
        response = requests.post(f"{base_url}/users", 
                               headers=headers, 
                               json=new_user)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   User created successfully")
        else:
            print(f"   Failed: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

def main():
    """Main test function"""
    print("SMS Transactions API - CRUD Operations Test")
    print("=" * 60)
    
    print("Make sure the server is running on http://localhost:8000")
    print("   Start it with: python start_simple.py")
    print()
    
    input("Press Enter when server is running...")
    
    # Test authentication
    test_authentication()
    
    # Test user management
    test_user_management()
    
    # Test CRUD operations
    crud_success = test_crud_operations()
    
    if crud_success:
        print("\nAll CRUD operations working correctly!")
    else:
        print("\nSome CRUD operations failed. Check the server logs.")

if __name__ == "__main__":
    main()
