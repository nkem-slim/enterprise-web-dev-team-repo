#!/usr/bin/env python3
"""
REST API Server for SMS Transactions
Built with Python's http.server module
"""

from http.server import HTTPServer
from controllers.transactions_controller import TransactionAPIHandler

def run_server(host='localhost', port=8000):
    """Run the HTTP server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    
    print(f"SMS Transactions REST API Server")
    print(f"Server running on http://{host}:{port}")
    print(f"API Documentation available at http://{host}:{port}")
    print(f"Available endpoints:")
    print(f"   GET    /transactions        - List all transactions")
    print(f"   GET    /transactions/{{id}}   - Get specific transaction")
    print(f"   POST   /transactions        - Create new transaction")
    print(f"   PUT    /transactions/{{id}}   - Update transaction")
    print(f"   DELETE /transactions/{{id}}   - Delete transaction")
    print(f"\n Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\nServer stopped")
        httpd.server_close()

if __name__ == '__main__':
    import sys
    
    # Parse command line arguments
    host = 'localhost'
    port = 8000
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    if len(sys.argv) > 2:
        host = sys.argv[2]
    
    run_server(host, port)
