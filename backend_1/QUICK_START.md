# Quick Start Guide

## Start the Server

### Option 1: Direct Python

```bash
cd backend_1
python server.py
```

### Option 2: Using the run script

```bash
cd backend_1
python run_server.py
```

### Option 3: Custom port

```bash
cd backend_1
python server.py 8080
```

## Test the API

### Test XML loading first

```bash
cd backend_1
python test_xml_loading.py
```

### Run automated tests

```bash
cd backend_1
python test_api.py
```

### Manual testing with curl

```bash
# Get all transactions
curl http://localhost:8000/transactions

# Get specific transaction
curl http://localhost:8000/transactions/txn_001

# Create new transaction
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "sender_name": "Test User",
    "receiver_name": "API Test",
    "amount": 1000.00,
    "transaction_type": "Transfer",
    "remarks": "Test transaction"
  }'
```

## API Endpoints

- `GET /` - API information
- `GET /transactions` - List all transactions
- `GET /transactions/{id}` - Get specific transaction
- `POST /transactions` - Create new transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

## Default Configuration

- **URL**: http://localhost:8000
- **Data**: In-memory storage (resets on restart)
- **Format**: JSON
- **CORS**: Enabled

## Files Created

- `server.py` - Main API server
- `test_api.py` - Automated tests
- `run_server.py` - Convenience runner
- `requirements.txt` - Dependencies (none required)
- `README.md` - Full documentation
- `start.bat` - Windows startup script
- `start.sh` - Linux/Mac startup script
