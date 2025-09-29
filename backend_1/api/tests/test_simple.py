#!/usr/bin/env python3
"""
Simple test to verify XML parsing
"""

import os
import sys
from api.models import Transaction, User
from api.controllers.user_controller import UserManager
from api.controllers.storage_controller import TransactionStorage
from api.controllers.transactions_controller import TransactionAPIHandler
from dsa.sms_parser import SMSXMLParser

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_xml_parsing():
    """Test XML parsing functionality"""
    print("Testing XML Parsing")
    print("=" * 30)

    # Check current directory
    print(f"Current directory: {os.getcwd()}")

    # Check if XML file exists in different locations
    paths_to_check = [
        "../modified_sms_v2.xml",
        "modified_sms_v2.xml",
        os.path.join("..", "modified_sms_v2.xml")
    ]

    xml_found = False
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"Found XML file at: {path}")
            xml_found = True
            break
        else:
            print(f"Not found: {path}")

    if not xml_found:
        print("XML file not found in any location")
        return False

    # Test parsing
    print("\nTesting XML parsing...")
    parser = SMSXMLParser()
    transactions = parser.parse_xml_file()

    if transactions:
        print(f"Successfully parsed {len(transactions)} transactions")

        # Show first few transactions
        print("\nFirst 3 transactions:")
        for i, txn in enumerate(transactions[:3]):
            print(
                f"  {i+1}. {txn.get('transaction_type', 'Unknown')} - {txn.get('amount', 0)} RWF")
            print(f"     From: {txn.get('sender_name', 'Unknown')}")
            print(f"     To: {txn.get('receiver_name', 'Unknown')}")
            print(f"     Date: {txn.get('transaction_date', 'Unknown')}")
            print()

        return True
    else:
        print("No transactions parsed")
        return False


if __name__ == "__main__":
    success = test_xml_parsing()
    if success:
        print("Test completed successfully!")
    else:
        print("Test failed!")
