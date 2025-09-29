from models import Transaction
from sms_parser import SMSXMLParser
from datetime import datetime

class TransactionStorage:
    """In-memory storage for transactions"""
    def __init__(self):
        self.transactions = {}
        self._load_sample_data()

    def _load_sample_data(self):
        """Load SMS transaction data from XML file or fallback to sample data"""
        # Try to parse the XML file first
        parser = SMSXMLParser()
        parsed_transactions = parser.parse_xml_file()
        
        if parsed_transactions:
            for txn_data in parsed_transactions:
                transaction = Transaction.from_dict(txn_data)
                # Only add if not already exists (prevents duplicates)
                if transaction.transaction_id not in self.transactions:
                    self.transactions[transaction.transaction_id] = transaction
        else:
            # Fallback to sample data
            sample_transactions = [
                {
                    'transaction_id': 'txn_001',
                    'sender_name': 'Jane Smith',
                    'receiver_name': 'Samuel Carter',
                    'amount': 2000.00,
                    'fee': 0.00,
                    'balance_after': 2000.00,
                    'transaction_date': '2024-05-10T16:30:51',
                    'transaction_type': 'Transfer',
                    'status': 'Completed',
                    'remarks': 'SMS: You have received 2000 RWF from Jane Smith'
                },
                {
                    'transaction_id': 'txn_002',
                    'sender_name': 'Samuel Carter',
                    'receiver_name': 'Jane Smith',
                    'amount': 1000.00,
                    'fee': 0.00,
                    'balance_after': 1000.00,
                    'transaction_date': '2024-05-10T16:31:39',
                    'transaction_type': 'Payment',
                    'status': 'Completed',
                    'remarks': 'SMS: TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith'
                },
                {
                    'transaction_id': 'txn_003',
                    'sender_name': 'Bank',
                    'receiver_name': 'Samuel Carter',
                    'amount': 40000.00,
                    'fee': 0.00,
                    'balance_after': 40400.00,
                    'transaction_date': '2024-05-11T18:43:49',
                    'transaction_type': 'Bank Deposit',
                    'status': 'Completed',
                    'remarks': 'SMS: A bank deposit of 40000 RWF has been added to your mobile money account'
                }
            ]
            
            for txn_data in sample_transactions:
                transaction = Transaction.from_dict(txn_data)
                self.transactions[transaction.transaction_id] = transaction

    def get_all(self):
        """Get all transactions"""
        return list(self.transactions.values())

    def get_by_id(self, transaction_id):
        """Get transaction by ID"""
        return self.transactions.get(transaction_id)

    def create(self, transaction):
        """Create new transaction"""
        if transaction.transaction_id in self.transactions:
            return None  # ID already exists
        self.transactions[transaction.transaction_id] = transaction
        return transaction

    def update(self, transaction_id, transaction_data):
        """Update existing transaction"""
        if transaction_id not in self.transactions:
            return None
        existing = self.transactions[transaction_id]
        
        # Update fields
        for key, value in transaction_data.items():
            if hasattr(existing, key) and key not in ['transaction_id', 'created_at']:
                setattr(existing, key, value)
        
        existing.updated_at = datetime.now().isoformat()
        return existing

    def delete(self, transaction_id):
        """Delete transaction"""
        if transaction_id not in self.transactions:
            return None
        return self.transactions.pop(transaction_id)
