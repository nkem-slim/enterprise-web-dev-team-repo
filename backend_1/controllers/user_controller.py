from models import User

class UserManager:
    """Manages user authentication"""
    def __init__(self):
        self.users = {}
        self._load_default_users()
    
    def _load_default_users(self):
        """Load default users"""
        default_users = [
            {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
            {'username': 'user', 'password': 'user123', 'role': 'user'},
            {'username': 'test', 'password': 'test123', 'role': 'user'}
        ]
        
        for user_data in default_users:
            user = User(user_data['username'], user_data['password'], user_data['role'])
            self.users[user.username] = user
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        if username in self.users:
            user = self.users[username]
            if user.password == password:
                return user
        return None
    
    def add_user(self, username, password, role="user"):
        """Add a new user"""
        if username in self.users:
            return False  # User already exists
        user = User(username, password, role)
        self.users[username] = user
        return True
    
    def get_user(self, username):
        """Get user by username"""
        return self.users.get(username)
