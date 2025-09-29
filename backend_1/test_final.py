#!/usr/bin/env python3
"""
Final test to verify everything works
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all imports"""
    print("Testing Imports")
    print("=" * 30)
    
    try:
        print("1. Testing models...")
        from models import Transaction, User
        print("   Models imported successfully")
        
        print("2. Testing user controller...")
        from controllers.user_controller import UserManager
        print("   User controller imported successfully")
        
        print("3. Testing storage controller...")
        from controllers.storage_controller import TransactionStorage
        print("   Storage controller imported successfully")
        
        print("4. Testing transactions controller...")
        from controllers.transactions_controller import TransactionAPIHandler
        print("   Transactions controller imported successfully")
        
        print("5. Testing SMS parser...")
        from sms_parser import SMSXMLParser
        print("   SMS parser imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_functionality():
    """Test basic functionality"""
    print("\nTesting Functionality")
    print("=" * 30)
    
    try:
        from models import Transaction, User
        from controllers.user_controller import UserManager
        from controllers.storage_controller import TransactionStorage
        from sms_parser import SMSXMLParser
        
        print("1. Testing user manager...")
        user_manager = UserManager()
        print(f"   User manager created with {len(user_manager.users)} users")
        
        print("2. Testing user authentication...")
        user = user_manager.authenticate("admin", "admin123")
        if user:
            print(f"   Admin authentication works: {user.username}")
        else:
            print("   Admin authentication failed")
        
        print("3. Testing storage...")
        storage = TransactionStorage()
        print(f"   Storage created with {len(storage.transactions)} transactions")
        
        print("4. Testing SMS parser...")
        parser = SMSXMLParser()
        transactions = parser.parse_xml_file()
        print(f"   SMS parser loaded {len(transactions)} transactions")
        
        return True
        
    except Exception as e:
        print(f"   Functionality error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("SMS Transactions API - Final Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test functionality
        functionality_ok = test_functionality()
        
        if functionality_ok:
            print("\nAll tests passed! The server should work now.")
            print("\nTo start the server, run:")
            print("   python server.py")
            print("   or")
            print("   start.bat")
        else:
            print("\nFunctionality tests failed.")
    else:
        print("\nImport tests failed.")

if __name__ == "__main__":
    main()
