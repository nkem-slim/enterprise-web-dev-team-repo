#!/usr/bin/env python3
"""
Test XML loading without starting HTTP server
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sms_parser import SMSXMLParser
from controllers.storage_controller import TransactionStorage

def test_xml_loading():
    """Test XML loading functionality"""
    print("Testing XML Loading")
    print("=" * 40)
    
    # Test parser directly
    print("1. Testing SMSXMLParser...")
    parser = SMSXMLParser()
    transactions = parser.parse_xml_file()
    
    if transactions:
        print(f"Parser found {len(transactions)} transactions")
        
        # Show transaction types
        types = {}
        for txn in transactions:
            txn_type = txn.get('transaction_type', 'Unknown')
            types[txn_type] = types.get(txn_type, 0) + 1
        
        print("Transaction types found:")
        for txn_type, count in sorted(types.items()):
            print(f"   {txn_type}: {count}")
        
        # Show first transaction
        if transactions:
            first = transactions[0]
            print(f"\nFirst transaction:")
            print(f"   Type: {first.get('transaction_type', 'Unknown')}")
            print(f"   Amount: {first.get('amount', 0)} RWF")
            print(f"   From: {first.get('sender_name', 'Unknown')}")
            print(f"   To: {first.get('receiver_name', 'Unknown')}")
            print(f"   Date: {first.get('transaction_date', 'Unknown')}")
    else:
        print("Parser found no transactions")
    
    # Test storage
    print("\n2. Testing TransactionStorage...")
    storage = TransactionStorage()
    all_transactions = storage.get_all()
    
    print(f"Storage loaded {len(all_transactions)} transactions")
    
    if all_transactions:
        print("Sample transactions from storage:")
        for i, txn in enumerate(all_transactions[:3]):
            print(f"   {i+1}. {txn.transaction_type} - {txn.amount} RWF")
    
    return len(all_transactions) > 0

if __name__ == "__main__":
    success = test_xml_loading()
    if success:
        print("\nXML loading test successful!")
    else:
        print("\nXML loading test failed!")
