#!/usr/bin/env python3
"""
Test script for XML parsing functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sms_parser import SMSXMLParser
import json

def test_xml_parsing():
    """Test the XML parsing functionality"""
    print("Testing XML Parsing Functionality")
    print("=" * 50)
    
    # Initialize parser
    parser = SMSXMLParser()
    
    # Parse the XML file
    print("Parsing XML file...")
    transactions = parser.parse_xml_file()
    
    if not transactions:
        print("No transactions found or parsing failed")
        return False
    
    print(f"Successfully parsed {len(transactions)} transactions")
    
    # Analyze transaction types
    transaction_types = {}
    for txn in transactions:
        txn_type = txn.get('transaction_type', 'Unknown')
        transaction_types[txn_type] = transaction_types.get(txn_type, 0) + 1
    
    print("\nTransaction Types Found:")
    for txn_type, count in sorted(transaction_types.items()):
        print(f"  {txn_type}: {count}")
    
    # Show sample transactions
    print(f"\nSample Transactions (first 5):")
    for i, txn in enumerate(transactions[:5]):
        print(f"\n  Transaction {i+1}:")
        print(f"    ID: {txn['transaction_id']}")
        print(f"    Type: {txn.get('transaction_type', 'Unknown')}")
        print(f"    Amount: {txn.get('amount', 0):.2f} RWF")
        print(f"    From: {txn.get('sender_name', 'Unknown')}")
        print(f"    To: {txn.get('receiver_name', 'Unknown')}")
        print(f"    Date: {txn.get('transaction_date', 'Unknown')}")
        print(f"    Remarks: {txn.get('remarks', 'None')[:50]}...")
    
    # Test specific patterns
    print(f"\nPattern Analysis:")
    patterns_found = {
        'Money Received': 0,
        'Payment': 0,
        'Bank Deposit': 0,
        'Transfer': 0,
        'Airtime Purchase': 0,
        'Cash Withdrawal': 0,
        'Merchant Payment': 0,
        'Unmatched': 0
    }
    
    for txn in transactions:
        txn_type = txn.get('transaction_type', 'Unmatched')
        if txn_type in patterns_found:
            patterns_found[txn_type] += 1
        else:
            patterns_found['Unmatched'] += 1
    
    for pattern, count in patterns_found.items():
        if count > 0:
            print(f"  {pattern}: {count}")
    
    # Save sample to file for inspection
    sample_file = "parsed_transactions_sample.json"
    with open(sample_file, 'w', encoding='utf-8') as f:
        json.dump(transactions[:10], f, indent=2, ensure_ascii=False)
    print(f"\nSample transactions saved to {sample_file}")
    
    return True

def test_regex_patterns():
    """Test individual regex patterns"""
    print("\nTesting Individual Regex Patterns")
    print("=" * 50)
    
    # Sample SMS messages for testing
    test_messages = [
        "You have received 2000 RWF from Jane Smith (*********013) on your mobile money account at 2024-05-10 16:30:51. Message from sender: . Your new balance:2000 RWF. Financial Transaction Id: 76662021700.",
        "TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845 has been completed at 2024-05-10 16:31:39. Your new balance: 1,000 RWF. Fee was 0 RWF.",
        "*113*R*A bank deposit of 40000 RWF has been added to your mobile money account at 2024-05-11 18:43:49. Your NEW BALANCE :40400 RWF.",
        "*165*S*10000 RWF transferred to Samuel Carter (250791666666) from 36521838 at 2024-05-11 20:34:47 . Fee was: 100 RWF. New balance: 28300 RWF.",
        "*162*TxId:13913173274*S*Your payment of 2000 RWF to Airtime with token  has been completed at 2024-05-12 11:41:28. Fee was 0 RWF. Your new balance: 25280 RWF ."
    ]
    
    parser = SMSXMLParser()
    
    for i, message in enumerate(test_messages):
        print(f"\n  Test Message {i+1}:")
        print(f"    Message: {message[:80]}...")
        
        # Test parsing
        result = parser._parse_sms_body(message, "2024-05-10T16:30:51", "10 May 2024 4:30:58 PM")
        
        if result:
            print(f"    Parsed successfully")
            print(f"    Type: {result.get('transaction_type', 'Unknown')}")
            print(f"    Amount: {result.get('amount', 0)}")
            print(f"    From: {result.get('sender_name', 'Unknown')}")
            print(f"    To: {result.get('receiver_name', 'Unknown')}")
        else:
            print(f"    Failed to parse")

def main():
    """Main test function"""
    print("SMS XML Parser Test Suite")
    print("=" * 60)
    
    # Test regex patterns first
    test_regex_patterns()
    
    # Test full XML parsing
    success = test_xml_parsing()
    
    if success:
        print("\nAll tests completed successfully!")
        print("\nYou can now run the server with:")
        print("   python server.py")
        print("\nThe server will load all parsed transactions from the XML file.")
    else:
        print("\nSome tests failed!")
        print("Check the XML file path and format.")

if __name__ == "__main__":
    main()
