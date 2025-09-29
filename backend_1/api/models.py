#!/usr/bin/env python3
"""
Data models for SMS Transactions API
"""

from datetime import datetime
import uuid
import hashlib

class User:
    """User data model for authentication"""
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password  # In real app, this should be hashed
        self.role = role
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at
        }

class Transaction:
    """Transaction data model"""
    def __init__(self, transaction_id=None, sender_name=None, receiver_name=None, 
                 amount=None, fee=0, balance_after=None, transaction_date=None, 
                 transaction_type=None, status="Completed", remarks=None):
        self.transaction_id = transaction_id or str(uuid.uuid4())
        self.sender_name = sender_name
        self.receiver_name = receiver_name
        self.amount = amount
        self.fee = fee
        self.balance_after = balance_after
        self.transaction_date = transaction_date or datetime.now().isoformat()
        self.transaction_type = transaction_type
        self.status = status
        self.remarks = remarks
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'sender_name': self.sender_name,
            'receiver_name': self.receiver_name,
            'amount': self.amount,
            'fee': self.fee,
            'balance_after': self.balance_after,
            'transaction_date': self.transaction_date,
            'transaction_type': self.transaction_type,
            'status': self.status,
            'remarks': self.remarks,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create transaction from dictionary"""
        transaction = cls()
        for key, value in data.items():
            if hasattr(transaction, key):
                setattr(transaction, key, value)
        return transaction
