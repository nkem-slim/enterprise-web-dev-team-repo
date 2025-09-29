#!/usr/bin/env python3
"""
Test script for SMS Transactions REST API
"""

import requests
import json
import time
import sys

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_connection(self):
        """Test if the API server is running"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("API server is running")
                return True
            else:
                print(f"API server returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("Cannot connect to API server. Make sure it's running on http://localhost:8000")
            return False
    
    def test_get_all_transactions(self):
        """Test GET /transactions endpoint"""
        print("\nTesting GET /transactions...")
        try:
            response = self.session.get(f"{self.base_url}/transactions")
            if response.status_code == 200:
                transactions = response.json()
                print(f"Retrieved {len(transactions)} transactions")
                return transactions
            else:
                print(f"Failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def test_get_specific_transaction(self, transaction_id):
        """Test GET /transactions/{id} endpoint"""
        print(f"\nTesting GET /transactions/{transaction_id}...")
        try:
            response = self.session.get(f"{self.base_url}/transactions/{transaction_id}")
            if response.status_code == 200:
                transaction = response.json()
                print(f"Retrieved transaction: {transaction['transaction_id']}")
                return transaction
            elif response.status_code == 404:
                print(f"Transaction {transaction_id} not found")
                return None
            else:
                print(f"Failed with status {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def test_create_transaction(self):
        """Test POST /transactions endpoint"""
        print("\nTesting POST /transactions...")
        new_transaction = {
            "sender_name": "Test User",
            "receiver_name": "API Test",
            "amount": 1500.00,
            "fee": 25.00,
            "balance_after": 3500.00,
            "transaction_type": "Test Transfer",
            "status": "Completed",
            "remarks": "Created via API test"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/transactions",
                headers={"Content-Type": "application/json"},
                data=json.dumps(new_transaction)
            )
            
            if response.status_code == 201:
                created_transaction = response.json()
                print(f"Created transaction: {created_transaction['transaction_id']}")
                return created_transaction
            else:
                print(f"Failed with status {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def test_update_transaction(self, transaction_id):
        """Test PUT /transactions/{id} endpoint"""
        print(f"\nTesting PUT /transactions/{transaction_id}...")
        update_data = {
            "amount": 2000.00,
            "status": "Updated",
            "remarks": "Updated via API test"
        }
        
        try:
            response = self.session.put(
                f"{self.base_url}/transactions/{transaction_id}",
                headers={"Content-Type": "application/json"},
                data=json.dumps(update_data)
            )
            
            if response.status_code == 200:
                updated_transaction = response.json()
                print(f"Updated transaction: {updated_transaction['transaction_id']}")
                return updated_transaction
            elif response.status_code == 404:
                print(f"Transaction {transaction_id} not found")
                return None
            else:
                print(f"Failed with status {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def test_delete_transaction(self, transaction_id):
        """Test DELETE /transactions/{id} endpoint"""
        print(f"\nTesting DELETE /transactions/{transaction_id}...")
        try:
            response = self.session.delete(f"{self.base_url}/transactions/{transaction_id}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Deleted transaction: {result['deleted_transaction']['transaction_id']}")
                return True
            elif response.status_code == 404:
                print(f"Transaction {transaction_id} not found")
                return False
            else:
                print(f"Failed with status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def test_error_cases(self):
        """Test error handling"""
        print("\nTesting error cases...")
        
        # Test invalid JSON
        print("  Testing invalid JSON...")
        try:
            response = self.session.post(
                f"{self.base_url}/transactions",
                headers={"Content-Type": "application/json"},
                data="invalid json"
            )
            if response.status_code == 400:
                print("  Invalid JSON handled correctly")
            else:
                print(f"  Expected 400, got {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Test missing required field
        print("  Testing missing required field...")
        try:
            invalid_transaction = {
                "sender_name": "Test User"
                # Missing required 'amount' field
            }
            response = self.session.post(
                f"{self.base_url}/transactions",
                headers={"Content-Type": "application/json"},
                data=json.dumps(invalid_transaction)
            )
            if response.status_code == 400:
                print("  Missing required field handled correctly")
            else:
                print(f"  Expected 400, got {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Test negative amount
        print("  Testing negative amount...")
        try:
            invalid_transaction = {
                "amount": -100.00
            }
            response = self.session.post(
                f"{self.base_url}/transactions",
                headers={"Content-Type": "application/json"},
                data=json.dumps(invalid_transaction)
            )
            if response.status_code == 400:
                print("  Negative amount handled correctly")
            else:
                print(f"  Expected 400, got {response.status_code}")
        except Exception as e:
            print(f"  Error: {e}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("Starting SMS Transactions API Tests")
        print("=" * 50)
        
        # Test connection
        if not self.test_connection():
            return False
        
        # Test GET all transactions
        transactions = self.test_get_all_transactions()
        if not transactions:
            return False
        
        # Test GET specific transaction (use first available)
        if transactions:
            first_transaction = transactions[0]
            self.test_get_specific_transaction(first_transaction['transaction_id'])
        
        # Test POST new transaction
        new_transaction = self.test_create_transaction()
        if not new_transaction:
            return False
        
        # Test PUT update transaction
        self.test_update_transaction(new_transaction['transaction_id'])
        
        # Test error cases
        self.test_error_cases()
        
        # Test DELETE transaction
        self.test_delete_transaction(new_transaction['transaction_id'])
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        return True

def main():
    """Main test function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    print(f"Testing API at: {base_url}")
    
    tester = APITester(base_url)
    success = tester.run_all_tests()
    
    if success:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
