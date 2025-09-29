#!/usr/bin/env python3
"""
Simple startup script for the SMS Transactions API
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the server"""
    try:
        print("Starting SMS Transactions REST API Server...")
        print("=" * 50)
        
        # Import and start server
        from server import run_server
        
        print("All imports successful!")
        print("Authentication enabled with default users:")
        print("   admin:admin123 (admin)")
        print("   user:user123 (user)")
        print("   test:test123 (user)")
        print()
        
        # Start server
        run_server()
        
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
