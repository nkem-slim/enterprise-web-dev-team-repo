from datetime import datetime
import uuid
import base64
import json
from http.server import BaseHTTPRequestHandler
from controllers.storage_controller import TransactionStorage
from controllers.user_controller import UserManager
from models import Transaction

class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API"""
    
    def __init__(self, *args, **kwargs):
        self.storage = TransactionStorage()
        self.user_manager = UserManager()
        super().__init__(*args, **kwargs)

    def _set_headers(self, status_code=200, content_type='application/json'):
        """Set HTTP response headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _authenticate_request(self):
        """Authenticate the incoming request"""
        auth_header = self.headers.get('Authorization', '')
        
        if not auth_header.startswith('Basic '):
            return None
        
        try:
            # Decode base64 credentials
            encoded_credentials = auth_header[6:]  # Remove 'Basic ' prefix
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            # Authenticate user
            user = self.user_manager.authenticate(username, password)
            return user
            
        except Exception as e:
            return None
    
    def _require_auth(self):
        """Check if request requires authentication and validate it"""
        user = self._authenticate_request()
        if not user:
            self._set_headers(401)
            error_response = {'error': 'Authentication required', 'message': 'Please provide valid username:password in Authorization header'}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
            return False
        return user

    def _parse_path(self):
        """Parse URL path and extract transaction ID if present"""
        path = self.path.split('?')[0]  # Remove query parameters
        parts = path.strip('/').split('/')
        
        if len(parts) == 2 and parts[0] == 'transactions':
            return 'transactions', parts[1] if parts[1] else None
        elif len(parts) == 1 and parts[0] == 'transactions':
            return 'transactions', None
        else:
            return None, None

    def _read_json_body(self):
        """Read and parse JSON from request body"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return None
            
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        except (ValueError, json.JSONDecodeError):
            return None

    def _validate_transaction_data(self, data):
        """Validate transaction data"""
        required_fields = ['amount']
        for field in required_fields:
            if field not in data or data[field] is None:
                return False, f"Missing required field: {field}"
        
        # Validate amount is positive
        try:
            amount = float(data['amount'])
            if amount <= 0:
                return False, "Amount must be positive"
        except (ValueError, TypeError):
            return False, "Amount must be a valid number"
        
        return True, None

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self._set_headers(200)
        self.wfile.write(b'')

    def do_GET(self):
        """Handle GET requests"""
        resource, resource_id = self._parse_path()
        
        if resource == 'transactions':
            # Require authentication for transaction endpoints
            user = self._require_auth()
            if not user:
                return
            
            if resource_id is None:
                # GET /transactions - List all transactions
                transactions = self.storage.get_all()
                response_data = [txn.to_dict() for txn in transactions]
                self._set_headers(200)
                self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
            else:
                # GET /transactions/{id} - Get specific transaction
                transaction = self.storage.get_by_id(resource_id)
                if transaction:
                    self._set_headers(200)
                    self.wfile.write(json.dumps(transaction.to_dict(), indent=2).encode('utf-8'))
                else:
                    self._set_headers(404)
                    error_response = {'error': 'Transaction not found'}
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
        elif resource == 'users':
            # GET /users - List users (admin only)
            user = self._require_auth()
            if not user:
                return
            
            if user.role != 'admin':
                self._set_headers(403)
                error_response = {'error': 'Admin access required'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            users_data = [u.to_dict() for u in self.user_manager.users.values()]
            self._set_headers(200)
            self.wfile.write(json.dumps(users_data, indent=2).encode('utf-8'))
        else:
            # Root endpoint - API info
            self._set_headers(200)
            api_info = {
                'message': 'SMS Transactions REST API',
                'version': '1.0.0',
                'authentication': 'Basic Auth (username:password)',
                'default_users': {
                    'admin': 'admin123',
                    'user': 'user123',
                    'test': 'test123'
                },
                'endpoints': {
                    'GET /transactions': 'List all transactions (Auth required)',
                    'GET /transactions/{id}': 'Get specific transaction (Auth required)',
                    'POST /transactions': 'Create new transaction (Auth required)',
                    'PUT /transactions/{id}': 'Update transaction (Auth required)',
                    'DELETE /transactions/{id}': 'Delete transaction (Auth required)',
                    'GET /users': 'List users (Admin only)',
                    'POST /users': 'Create new user (Admin only)'
                }
            }
            self.wfile.write(json.dumps(api_info, indent=2).encode('utf-8'))

    def do_POST(self):
        """Handle POST requests"""
        resource, resource_id = self._parse_path()
        
        if resource == 'transactions' and resource_id is None:
            # POST /transactions - Create new transaction
            user = self._require_auth()
            if not user:
                return
            
            data = self._read_json_body()
            if data is None:
                self._set_headers(400)
                error_response = {'error': 'Invalid JSON data'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            # Validate data
            is_valid, error_message = self._validate_transaction_data(data)
            if not is_valid:
                self._set_headers(400)
                error_response = {'error': error_message}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            # Create transaction
            transaction = Transaction.from_dict(data)
            created_transaction = self.storage.create(transaction)
            
            if created_transaction:
                self._set_headers(201)
                self.wfile.write(json.dumps(created_transaction.to_dict(), indent=2).encode('utf-8'))
            else:
                self._set_headers(409)
                error_response = {'error': 'Transaction ID already exists'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        elif resource == 'users' and resource_id is None:
            # POST /users - Create new user (admin only)
            user = self._require_auth()
            if not user:
                return
            
            if user.role != 'admin':
                self._set_headers(403)
                error_response = {'error': 'Admin access required'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            data = self._read_json_body()
            if data is None:
                self._set_headers(400)
                error_response = {'error': 'Invalid JSON data'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            # Validate required fields
            if 'username' not in data or 'password' not in data:
                self._set_headers(400)
                error_response = {'error': 'Username and password are required'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            # Create user
            role = data.get('role', 'user')
            success = self.user_manager.add_user(data['username'], data['password'], role)
            
            if success:
                new_user = self.user_manager.get_user(data['username'])
                self._set_headers(201)
                self.wfile.write(json.dumps(new_user.to_dict(), indent=2).encode('utf-8'))
            else:
                self._set_headers(409)
                error_response = {'error': 'Username already exists'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self._set_headers(404)
            error_response = {'error': 'Endpoint not found'}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_PUT(self):
        """Handle PUT requests"""
        resource, resource_id = self._parse_path()
        
        if resource == 'transactions' and resource_id:
            # PUT /transactions/{id} - Update transaction
            user = self._require_auth()
            if not user:
                return
            
            data = self._read_json_body()
            if data is None:
                self._set_headers(400)
                error_response = {'error': 'Invalid JSON data'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
                return
            
            # Validate data if amount is provided
            if 'amount' in data:
                is_valid, error_message = self._validate_transaction_data(data)
                if not is_valid:
                    self._set_headers(400)
                    error_response = {'error': error_message}
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
                    return
            
            # Update transaction
            updated_transaction = self.storage.update(resource_id, data)
            if updated_transaction:
                self._set_headers(200)
                self.wfile.write(json.dumps(updated_transaction.to_dict(), indent=2).encode('utf-8'))
            else:
                self._set_headers(404)
                error_response = {'error': 'Transaction not found'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self._set_headers(404)
            error_response = {'error': 'Endpoint not found'}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def do_DELETE(self):
        """Handle DELETE requests"""
        resource, resource_id = self._parse_path()
        
        if resource == 'transactions' and resource_id:
            # DELETE /transactions/{id} - Delete transaction
            user = self._require_auth()
            if not user:
                return
            
            deleted_transaction = self.storage.delete(resource_id)
            if deleted_transaction:
                self._set_headers(200)
                response_data = {'message': 'Transaction deleted successfully', 'deleted_transaction': deleted_transaction.to_dict()}
                self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
            else:
                self._set_headers(404)
                error_response = {'error': 'Transaction not found'}
                self.wfile.write(json.dumps(error_response).encode('utf-8'))
        else:
            self._set_headers(404)
            error_response = {'error': 'Endpoint not found'}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

    def log_message(self, format, *args):
        """Override to customize log format"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")
