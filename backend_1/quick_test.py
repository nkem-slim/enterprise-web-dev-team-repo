#!/usr/bin/env python3
"""
Quick test to verify basic functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work"""
    print("Testing Imports...")
    
    try:
        from models import Transaction, User
        print("Models imported")
        
        from controllers.user_controller import UserManager
        print("User controller imported")
        
        from controllers.storage_controller import TransactionStorage
        print("Storage controller imported")
        
        from controllers.transactions_controller import TransactionAPIHandler
        print("Transactions controller imported")
        
        return True
    except Exception as e:
        print(f"Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without server"""
    print("\nTesting Basic Functionality...")
    
    try:
        from models import Transaction, User
        from controllers.user_controller import UserManager
        from controllers.storage_controller import TransactionStorage
        
        # Test user manager
        user_manager = UserManager()
        print(f"User manager: {len(user_manager.users)} users")
        
        # Test authentication
        user = user_manager.authenticate("admin", "admin123")
        if user:
            print(f"Authentication works: {user.username} ({user.role})")
        else:
            print("Authentication failed")
            return False
        
        # Test storage
        storage = TransactionStorage()
        print(f"Storage: {len(storage.transactions)} transactions")
        
        # Test CRUD operations
        print("\nTesting CRUD Operations...")
        
        # Create
        test_txn = Transaction(
            sender_name="Test Sender",
            receiver_name="Test Receiver",
            amount=100.0,
            transaction_type="Test"
        )
        created = storage.create(test_txn)
        if created:
            print("CREATE works")
            txn_id = created.transaction_id
        else:
            print("CREATE failed")
            return False
        
        # Read
        retrieved = storage.get_by_id(txn_id)
        if retrieved and retrieved.amount == 100.0:
            print("READ works")
        else:
            print("READ failed")
            return False
        
        # Update
        updated = storage.update(txn_id, {"amount": 200.0, "status": "Updated"})
        if updated and updated.amount == 200.0:
            print("UPDATE works")
        else:
            print("UPDATE failed")
            return False
        
        # Delete
        deleted = storage.delete(txn_id)
        if deleted:
            print("DELETE works")
        else:
            print("DELETE failed")
            return False
        
        # Verify deletion
        not_found = storage.get_by_id(txn_id)
        if not_found is None:
            print("DELETE verification works")
        else:
            print("DELETE verification failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"Functionality error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("Quick Test - SMS Transactions API")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\nImport test failed. Check the error messages above.")
        return
    
    # Test functionality
    if test_basic_functionality():
        print("\nAll tests passed! The CRUD operations are working correctly.")
        print("\nTo test the full server:")
        print("1. Run: python test_server_startup.py")
        print("2. Then run: python test_crud_operations.py")
    else:
        print("\nFunctionality test failed. Check the error messages above.")

if __name__ == "__main__":
    main()