#!/usr/bin/env python3
"""
Test server startup and basic functionality
"""

import sys
import os
import threading
import time
import requests
import base64

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_auth_header(username, password):
    """Create Basic Auth header"""
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f"Basic {encoded_credentials}"

def start_server():
    """Start the server in a separate thread"""
    try:
        from server import run_server
        print("Starting server in background...")
        run_server()
    except Exception as e:
        print(f"Server error: {e}")

def test_server():
    """Test if server is responding"""
    base_url = "http://localhost:8000"
    
    print("Testing Server Response")
    print("=" * 30)
    
    # Wait a moment for server to start
    time.sleep(2)
    
    try:
        # Test root endpoint (no auth required)
        print("1. Testing root endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Server responding: {data.get('message', 'Unknown')}")
        else:
            print(f"   Root endpoint failed")
            return False
        
        # Test transactions endpoint (auth required)
        print("2. Testing transactions endpoint...")
        headers = {"Authorization": create_auth_header("admin", "admin123")}
        response = requests.get(f"{base_url}/transactions", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Transactions endpoint working: {len(data)} transactions")
        else:
            print(f"   Transactions endpoint failed: {response.text}")
            return False
        
        # Test user management
        print("3. Testing user management...")
        response = requests.get(f"{base_url}/users", headers=headers, timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   User management working: {len(data)} users")
        else:
            print(f"   User management failed: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("   Connection failed - Server not responding")
        return False
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    """Main test function"""
    print("SMS Transactions API - Server Startup Test")
    print("=" * 50)
    
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Test server
    success = test_server()
    
    if success:
        print("\nServer is working correctly!")
        print("You can now run: python test_crud_operations.py")
    else:
        print("\nServer has issues. Check the error messages above.")
    
    print("\nPress Ctrl+C to stop the server...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTest completed")

if __name__ == "__main__":
    main()
