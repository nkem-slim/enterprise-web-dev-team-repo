#!/usr/bin/env python3
"""
Test script to check imports
"""

try:
    print("Testing imports...")
    
    print("1. Testing models import...")
    from models import Transaction, User
    print("   Models imported successfully")
    
    print("2. Testing user controller import...")
    from controllers.user_controller import UserManager
    print("   User controller imported successfully")
    
    print("3. Testing storage controller import...")
    from controllers.storage_controller import TransactionStorage
    print("   Storage controller imported successfully")
    
    print("4. Testing transactions controller import...")
    from controllers.transactions_controller import TransactionAPIHandler
    print("   Transactions controller imported successfully")
    
    print("5. Testing server import...")
    from server import run_server
    print("   Server imported successfully")
    
    print("\nAll imports successful!")
    
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
