# SMS Transactions REST API

A simple REST API server built with Python's `http.server` module for managing SMS transaction data.

## Features

- **Pure Python**: Built using only Python standard library modules
- **RESTful API**: Full CRUD operations for transaction management
- **Authentication**: Basic Auth with username/password
- **User Management**: Create and manage users (admin only)
- **CORS Support**: Cross-origin requests enabled
- **JSON API**: All requests and responses use JSON format
- **In-Memory Storage**: Data persists during server session
- **XML Parsing**: Automatically extracts transactions from SMS XML files
- **Regex-Based Parsing**: Advanced pattern matching for different transaction types
- **Sample Data**: Pre-loaded with sample SMS transaction data (fallback)

## Quick Start

### Prerequisites

- Python 3.6 or higher
- No external dependencies required

### Installation

1. Navigate to the backend_1 directory:

   ```bash
   cd backend_1
   ```

2. Run the server:

   ```bash
   python server.py
   ```

3. Or specify custom host and port:
   ```bash
   python server.py 8080 localhost
   ```

### XML Data Loading

The server automatically attempts to load transaction data from the XML file (`../modified_sms_v2.xml`). If the file is not found or parsing fails, it falls back to sample data.

**Supported Transaction Types:**

- Money Received
- Payment
- Bank Deposit
- Transfer
- Airtime Purchase
- Cash Withdrawal
- Merchant Payment

**Testing XML Parsing:**

```bash
python test_xml_parser.py
```

### Default Configuration

- **Host**: localhost
- **Port**: 8000
- **Base URL**: http://localhost:8000
- **Authentication**: Basic Auth (username:password)

### Default Users

| Username | Password | Role  | Access                        |
| -------- | -------- | ----- | ----------------------------- |
| admin    | admin123 | admin | Full access + user management |
| user     | user123  | user  | Transaction operations only   |
| test     | test123  | user  | Transaction operations only   |

## API Endpoints

### 1. Get API Information

```
GET /
```

Returns API documentation and available endpoints.

### 2. List All Transactions

```
GET /transactions
```

Returns a list of all SMS transactions.

**Response:**

```json
[
  {
    "transaction_id": "txn_001",
    "sender_name": "Jane Smith",
    "receiver_name": "Samuel Carter",
    "amount": 2000.0,
    "fee": 0.0,
    "balance_after": 2000.0,
    "transaction_date": "2024-05-10T16:30:51",
    "transaction_type": "Transfer",
    "status": "Completed",
    "remarks": "SMS: You have received 2000 RWF from Jane Smith",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

### 3. Get Specific Transaction

```
GET /transactions/{id}
```

Returns details of a specific transaction.

**Response:**

```json
{
  "transaction_id": "txn_001",
  "sender_name": "Jane Smith",
  "receiver_name": "Samuel Carter",
  "amount": 2000.0,
  "fee": 0.0,
  "balance_after": 2000.0,
  "transaction_date": "2024-05-10T16:30:51",
  "transaction_type": "Transfer",
  "status": "Completed",
  "remarks": "SMS: You have received 2000 RWF from Jane Smith",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### 4. Create New Transaction

```
POST /transactions
```

Creates a new SMS transaction.

**Request Body:**

```json
{
  "sender_name": "John Doe",
  "receiver_name": "Jane Smith",
  "amount": 1500.0,
  "fee": 10.0,
  "balance_after": 3500.0,
  "transaction_date": "2024-01-15T14:30:00",
  "transaction_type": "Payment",
  "status": "Completed",
  "remarks": "SMS: Payment to Jane Smith"
}
```

**Response:** 201 Created with the created transaction data.

### 5. Update Transaction

```
PUT /transactions/{id}
```

Updates an existing transaction.

**Request Body:**

```json
{
  "amount": 2000.0,
  "status": "Failed",
  "remarks": "Updated transaction details"
}
```

**Response:** 200 OK with updated transaction data.

### 6. Delete Transaction

```
DELETE /transactions/{id}
```

Deletes a specific transaction.

**Response:**

```json
{
  "message": "Transaction deleted successfully",
  "deleted_transaction": {
    "transaction_id": "txn_001",
    "sender_name": "Jane Smith",
    "receiver_name": "Samuel Carter",
    "amount": 2000.0,
    "fee": 0.0,
    "balance_after": 2000.0,
    "transaction_date": "2024-05-10T16:30:51",
    "transaction_type": "Transfer",
    "status": "Completed",
    "remarks": "SMS: You have received 2000 RWF from Jane Smith",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

## Data Model

### Transaction Fields

| Field              | Type   | Required | Description                               |
| ------------------ | ------ | -------- | ----------------------------------------- |
| `transaction_id`   | String | Auto     | Unique identifier (UUID)                  |
| `sender_name`      | String | No       | Name of sender                            |
| `receiver_name`    | String | No       | Name of receiver                          |
| `amount`           | Number | Yes      | Transaction amount (must be positive)     |
| `fee`              | Number | No       | Transaction fee (default: 0)              |
| `balance_after`    | Number | No       | Account balance after transaction         |
| `transaction_date` | String | No       | Transaction timestamp (ISO format)        |
| `transaction_type` | String | No       | Type of transaction                       |
| `status`           | String | No       | Transaction status (default: "Completed") |
| `remarks`          | String | No       | Additional notes                          |
| `created_at`       | String | Auto     | Creation timestamp                        |
| `updated_at`       | String | Auto     | Last update timestamp                     |

## Error Responses

### 400 Bad Request

```json
{
  "error": "Invalid JSON data"
}
```

### 404 Not Found

```json
{
  "error": "Transaction not found"
}
```

### 409 Conflict

```json
{
  "error": "Transaction ID already exists"
}
```

## Testing the API

### Using curl

1. **Get all transactions:**

   ```bash
   curl http://localhost:8000/transactions
   ```

2. **Get specific transaction:**

   ```bash
   curl http://localhost:8000/transactions/txn_001
   ```

3. **Create new transaction:**

   ```bash
   curl -X POST http://localhost:8000/transactions \
     -H "Content-Type: application/json" \
     -d '{
       "sender_name": "Test User",
       "receiver_name": "Another User",
       "amount": 1000.00,
       "transaction_type": "Transfer",
       "remarks": "Test transaction"
     }'
   ```

4. **Update transaction:**

   ```bash
   curl -X PUT http://localhost:8000/transactions/txn_001 \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 2500.00,
       "status": "Completed"
     }'
   ```

5. **Delete transaction:**
   ```bash
   curl -X DELETE http://localhost:8000/transactions/txn_001
   ```

### Using Python requests

```python
import requests
import json

base_url = "http://localhost:8000"

# Get all transactions
response = requests.get(f"{base_url}/transactions")
print(response.json())

# Create new transaction
new_transaction = {
    "sender_name": "Python User",
    "receiver_name": "API Test",
    "amount": 500.00,
    "transaction_type": "Payment",
    "remarks": "Created via Python"
}

response = requests.post(
    f"{base_url}/transactions",
    headers={"Content-Type": "application/json"},
    data=json.dumps(new_transaction)
)
print(response.json())
```

## Architecture

### Components

1. **Transaction Class**: Data model for SMS transactions
2. **TransactionStorage Class**: In-memory storage and data management
3. **TransactionAPIHandler Class**: HTTP request handler with CRUD operations
4. **Main Server**: HTTP server setup and execution

### Key Features

- **RESTful Design**: Follows REST principles with proper HTTP methods
- **Error Handling**: Comprehensive error responses with appropriate status codes
- **Data Validation**: Input validation for required fields and data types
- **CORS Support**: Cross-origin resource sharing enabled
- **Logging**: Request logging with timestamps
- **UUID Generation**: Automatic unique ID generation for new transactions

## Development Notes

- Built using Python's `http.server` module for simplicity
- No external dependencies required
- In-memory storage (data lost on server restart)
- Suitable for development, testing, and small-scale applications
- Can be extended with database persistence, authentication, and additional features

## Future Enhancements

- Database persistence (SQLite, PostgreSQL, MongoDB)
- Authentication and authorization
- Input validation with schema validation
- Pagination for large datasets
- Search and filtering capabilities
- Rate limiting
- API versioning
- Comprehensive logging and monitoring
