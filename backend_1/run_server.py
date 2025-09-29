#!/usr/bin/env python3
"""
Convenience script to run the SMS Transactions REST API server
"""

import sys
import os
import subprocess
import time
import signal
import threading
from server import run_server

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_port_available(host, port):
    """Check if the port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            return True
    except OSError:
        return False

def start_server(host='localhost', port=8000):
    """Start the server with error handling"""
    print("SMS Transactions REST API Server")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check if port is available
    if not check_port_available(host, port):
        print(f"Port {port} is already in use")
        print(f"Try a different port: python run_server.py {port + 1}")
        return False
    
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Port {port} is available")
    print(f"Starting server on {host}:{port}")
    
    try:
        # Start the server
        run_server(host, port)
    except KeyboardInterrupt:
        print(f"\nServer stopped by user")
        return True
    except Exception as e:
        print(f"Server error: {e}")
        return False

def show_help():
    """Show help information"""
    print("SMS Transactions REST API Server")
    print("=" * 40)
    print("Usage:")
    print("  python run_server.py [port] [host]")
    print("")
    print("Examples:")
    print("  python run_server.py                    # Run on localhost:8000")
    print("  python run_server.py 8080               # Run on localhost:8080")
    print("  python run_server.py 8080 0.0.0.0       # Run on all interfaces:8080")
    print("")
    print("Options:")
    print("  -h, --help     Show this help message")
    print("  -v, --version  Show version information")
    print("")
    print("Endpoints:")
    print("  GET    /transactions        - List all transactions")
    print("  GET    /transactions/{id}   - Get specific transaction")
    print("  POST   /transactions        - Create new transaction")
    print("  PUT    /transactions/{id}   - Update transaction")
    print("  DELETE /transactions/{id}   - Delete transaction")
    print("")
    print("Testing:")
    print("  python test_api.py         - Run API tests")

def show_version():
    """Show version information"""
    print("SMS Transactions REST API v1.0.0")
    print("Built with Python http.server")
    print(f"Python version: {sys.version}")

def main():
    """Main function"""
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            show_help()
            return
        elif sys.argv[1] in ['-v', '--version']:
            show_version()
            return
    
    # Get port and host from arguments
    port = 8000
    host = 'localhost'
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print("Use -h for help")
            return
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    # Start the server
    success = start_server(host, port)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
