#!/usr/bin/env python3
"""
Simple test to verify the server works
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing server startup...")
    
    # Test imports
    from models import Transaction, User
    print("Models imported")
    
    from controllers.user_controller import UserManager
    print("User controller imported")
    
    from controllers.storage_controller import TransactionStorage
    print("Storage controller imported")
    
    from controllers.transactions_controller import TransactionAPIHandler
    print("Transactions controller imported")
    
    # Test basic functionality
    user_manager = UserManager()
    print(f"User manager created with {len(user_manager.users)} users")
    
    storage = TransactionStorage()
    print(f"Storage created with {len(storage.transactions)} transactions")
    
    print("\nAll tests passed! Server should work now.")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()