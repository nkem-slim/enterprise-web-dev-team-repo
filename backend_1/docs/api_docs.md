# SMS Transactions REST API Documentation

## Overview

The SMS Transactions API is a RESTful service for managing financial transactions extracted from SMS messages. It provides full CRUD operations for transactions and user management with role-based authentication.

**Base URL:** `http://localhost:8000`  
**Authentication:** Basic Auth (username:password)  
**Content-Type:** `application/json`  
**CORS:** Enabled for all origins

## Authentication

All endpoints except the root endpoint require Basic Authentication. Include the `Authorization` header with base64-encoded credentials:

```
Authorization: Basic <base64(username:password)>
```

### Default Users

| Username | Password | Role  | Access                        |
| -------- | -------- | ----- | ----------------------------- |
| admin    | admin123 | admin | Full access + user management |
| user     | user123  | user  | Transaction operations only   |
| test     | test123  | user  | Transaction operations only   |

## Endpoints

### 1. API Information

#### GET /

Get API information and available endpoints.

**Authentication:** None required

**Request Example:**

```bash
curl http://localhost:8000/
```

**Response Example:**

```json
{
  "message": "SMS Transactions REST API",
  "version": "1.0.0",
  "authentication": "Basic Auth (username:password)",
  "default_users": {
    "admin": "admin123",
    "user": "user123",
    "test": "test123"
  },
  "endpoints": {
    "GET /transactions": "List all transactions (Auth required)",
    "GET /transactions/{id}": "Get specific transaction (Auth required)",
    "POST /transactions": "Create new transaction (Auth required)",
    "PUT /transactions/{id}": "Update transaction (Auth required)",
    "DELETE /transactions/{id}": "Delete transaction (Auth required)",
    "GET /users": "List users (Admin only)",
    "POST /users": "Create new user (Admin only)"
  }
}
```

---

### 2. Transaction Management

#### GET /transactions

List all transactions.

**Authentication:** Required

**Request Example:**

```bash
curl -u admin:admin123 http://localhost:8000/transactions
```

**Response Example:**

```json
[
  {
    "transaction_id": "txn_abc123",
    "sender_name": "John Doe",
    "receiver_name": "Jane Smith",
    "amount": 1000.5,
    "fee": 25.0,
    "balance_after": 5000.0,
    "transaction_date": "2024-01-15T10:30:00",
    "transaction_type": "Transfer",
    "status": "Completed",
    "remarks": "Payment for services",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

#### GET /transactions/{id}

Get a specific transaction by ID.

**Authentication:** Required

**Request Example:**

```bash
curl -u admin:admin123 http://localhost:8000/transactions/txn_abc123
```

**Response Example:**

```json
{
  "transaction_id": "txn_abc123",
  "sender_name": "John Doe",
  "receiver_name": "Jane Smith",
  "amount": 1000.5,
  "fee": 25.0,
  "balance_after": 5000.0,
  "transaction_date": "2024-01-15T10:30:00",
  "transaction_type": "Transfer",
  "status": "Completed",
  "remarks": "Payment for services",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### POST /transactions

Create a new transaction.

**Authentication:** Required

**Request Example:**

```bash
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "sender_name": "John Doe",
    "receiver_name": "Jane Smith",
    "amount": 1000.50,
    "fee": 25.00,
    "balance_after": 5000.00,
    "transaction_type": "Transfer",
    "status": "Completed",
    "remarks": "Payment for services"
  }' \
  http://localhost:8000/transactions
```

**Request Body:**

```json
{
  "sender_name": "John Doe",
  "receiver_name": "Jane Smith",
  "amount": 1000.5,
  "fee": 25.0,
  "balance_after": 5000.0,
  "transaction_type": "Transfer",
  "status": "Completed",
  "remarks": "Payment for services"
}
```

**Required Fields:**

- `amount` (number): Transaction amount (must be positive)

**Optional Fields:**

- `sender_name` (string): Name of the sender
- `receiver_name` (string): Name of the receiver
- `fee` (number): Transaction fee (default: 0)
- `balance_after` (number): Account balance after transaction
- `transaction_date` (string): Transaction date (ISO format, defaults to current time)
- `transaction_type` (string): Type of transaction
- `status` (string): Transaction status (default: "Completed")
- `remarks` (string): Additional remarks

**Response Example:**

```json
{
  "transaction_id": "txn_abc123",
  "sender_name": "John Doe",
  "receiver_name": "Jane Smith",
  "amount": 1000.5,
  "fee": 25.0,
  "balance_after": 5000.0,
  "transaction_date": "2024-01-15T10:30:00",
  "transaction_type": "Transfer",
  "status": "Completed",
  "remarks": "Payment for services",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### PUT /transactions/{id}

Update an existing transaction.

**Authentication:** Required

**Request Example:**

```bash
curl -X PUT -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1500.00,
    "status": "Pending",
    "remarks": "Updated payment"
  }' \
  http://localhost:8000/transactions/txn_abc123
```

**Request Body:**

```json
{
  "amount": 1500.0,
  "status": "Pending",
  "remarks": "Updated payment"
}
```

**Note:** Only provide the fields you want to update. All fields are optional.

**Response Example:**

```json
{
  "transaction_id": "txn_abc123",
  "sender_name": "John Doe",
  "receiver_name": "Jane Smith",
  "amount": 1500.0,
  "fee": 25.0,
  "balance_after": 5000.0,
  "transaction_date": "2024-01-15T10:30:00",
  "transaction_type": "Transfer",
  "status": "Pending",
  "remarks": "Updated payment",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

#### DELETE /transactions/{id}

Delete a transaction.

**Authentication:** Required

**Request Example:**

```bash
curl -X DELETE -u admin:admin123 http://localhost:8000/transactions/txn_abc123
```

**Response Example:**

```json
{
  "message": "Transaction deleted successfully",
  "deleted_transaction": {
    "transaction_id": "txn_abc123",
    "sender_name": "John Doe",
    "receiver_name": "Jane Smith",
    "amount": 1000.5,
    "fee": 25.0,
    "balance_after": 5000.0,
    "transaction_date": "2024-01-15T10:30:00",
    "transaction_type": "Transfer",
    "status": "Completed",
    "remarks": "Payment for services",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

---

### 3. User Management

#### GET /users

List all users (Admin only).

**Authentication:** Required (Admin role)

**Request Example:**

```bash
curl -u admin:admin123 http://localhost:8000/users
```

**Response Example:**

```json
[
  {
    "username": "admin",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "username": "user",
    "role": "user",
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "username": "test",
    "role": "user",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### POST /users

Create a new user (Admin only).

**Authentication:** Required (Admin role)

**Request Example:**

```bash
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "newpass123",
    "role": "user"
  }' \
  http://localhost:8000/users
```

**Request Body:**

```json
{
  "username": "newuser",
  "password": "newpass123",
  "role": "user"
}
```

**Required Fields:**

- `username` (string): Unique username
- `password` (string): User password

**Optional Fields:**

- `role` (string): User role (default: "user")

**Response Example:**

```json
{
  "username": "newuser",
  "role": "user",
  "created_at": "2024-01-15T12:00:00"
}
```

---

## Error Codes

### HTTP Status Codes

| Code | Status                | Description                       |
| ---- | --------------------- | --------------------------------- |
| 200  | OK                    | Request successful                |
| 201  | Created               | Resource created successfully     |
| 400  | Bad Request           | Invalid request data              |
| 401  | Unauthorized          | Authentication required or failed |
| 403  | Forbidden             | Insufficient permissions          |
| 404  | Not Found             | Resource not found                |
| 409  | Conflict              | Resource already exists           |
| 500  | Internal Server Error | Server error                      |

### Error Response Format

All error responses follow this format:

```json
{
  "error": "Error message description"
}
```

### Common Error Responses

#### 400 Bad Request

```json
{
  "error": "Invalid JSON data"
}
```

```json
{
  "error": "Missing required field: amount"
}
```

```json
{
  "error": "Amount must be positive"
}
```

#### 401 Unauthorized

```json
{
  "error": "Authentication required",
  "message": "Please provide valid username:password in Authorization header"
}
```

#### 403 Forbidden

```json
{
  "error": "Admin access required"
}
```

#### 404 Not Found

```json
{
  "error": "Transaction not found"
}
```

```json
{
  "error": "Endpoint not found"
}
```

#### 409 Conflict

```json
{
  "error": "Transaction ID already exists"
}
```

```json
{
  "error": "Username already exists"
}
```

---

## Data Models

### Transaction

| Field            | Type   | Required | Description                               |
| ---------------- | ------ | -------- | ----------------------------------------- |
| transaction_id   | string | No       | Unique identifier (auto-generated)        |
| sender_name      | string | No       | Name of the sender                        |
| receiver_name    | string | No       | Name of the receiver                      |
| amount           | number | Yes      | Transaction amount (must be positive)     |
| fee              | number | No       | Transaction fee (default: 0)              |
| balance_after    | number | No       | Account balance after transaction         |
| transaction_date | string | No       | Transaction date (ISO format)             |
| transaction_type | string | No       | Type of transaction                       |
| status           | string | No       | Transaction status (default: "Completed") |
| remarks          | string | No       | Additional remarks                        |
| created_at       | string | No       | Creation timestamp (ISO format)           |
| updated_at       | string | No       | Last update timestamp (ISO format)        |

### User

| Field      | Type   | Required | Description                     |
| ---------- | ------ | -------- | ------------------------------- |
| username   | string | Yes      | Unique username                 |
| password   | string | Yes      | User password                   |
| role       | string | No       | User role (default: "user")     |
| created_at | string | No       | Creation timestamp (ISO format) |

---

## Examples

### JavaScript (Fetch API)

```javascript
// Get all transactions
const response = await fetch("http://localhost:8000/transactions", {
  headers: {
    Authorization: "Basic " + btoa("admin:admin123"),
  },
});
const transactions = await response.json();

// Create a new transaction
const newTransaction = await fetch("http://localhost:8000/transactions", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Basic " + btoa("admin:admin123"),
  },
  body: JSON.stringify({
    sender_name: "John Doe",
    receiver_name: "Jane Smith",
    amount: 1000.5,
    transaction_type: "Transfer",
  }),
});
```

### Python (requests)

```python
import requests
import base64

# Authentication
auth = ('admin', 'admin123')

# Get all transactions
response = requests.get('http://localhost:8000/transactions', auth=auth)
transactions = response.json()

# Create a new transaction
new_transaction = {
    'sender_name': 'John Doe',
    'receiver_name': 'Jane Smith',
    'amount': 1000.50,
    'transaction_type': 'Transfer'
}
response = requests.post('http://localhost:8000/transactions',
                        json=new_transaction, auth=auth)
```

### cURL Examples

```bash
# Get API info
curl http://localhost:8000/

# List transactions
curl -u admin:admin123 http://localhost:8000/transactions

# Get specific transaction
curl -u admin:admin123 http://localhost:8000/transactions/txn_abc123

# Create transaction
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"amount": 1000.50, "sender_name": "John Doe"}' \
  http://localhost:8000/transactions

# Update transaction
curl -X PUT -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"amount": 1500.00}' \
  http://localhost:8000/transactions/txn_abc123

# Delete transaction
curl -X DELETE -u admin:admin123 http://localhost:8000/transactions/txn_abc123

# List users (admin only)
curl -u admin:admin123 http://localhost:8000/users

# Create user (admin only)
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"username": "newuser", "password": "newpass123"}' \
  http://localhost:8000/users
```

---

## CORS Support

The API supports Cross-Origin Resource Sharing (CORS) with the following configuration:

- **Access-Control-Allow-Origin:** `*` (all origins)
- **Access-Control-Allow-Methods:** `GET, POST, PUT, DELETE, OPTIONS`
- **Access-Control-Allow-Headers:** `Content-Type, Authorization`

## Rate Limiting

Currently, no rate limiting is implemented. In production, consider implementing rate limiting to prevent abuse.

## Security Notes

1. **Password Storage:** Passwords are stored in plain text for simplicity. In production, use proper password hashing (bcrypt, scrypt, etc.).

2. **Authentication:** Basic Auth is used for simplicity. In production, consider using JWT tokens or OAuth2.

3. **HTTPS:** Always use HTTPS in production to protect credentials and data in transit.

4. **Input Validation:** Basic validation is implemented. Consider adding more comprehensive validation for production use.

5. **Error Handling:** Avoid exposing sensitive information in error messages in production.
