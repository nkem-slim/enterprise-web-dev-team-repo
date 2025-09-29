import re
from datetime import datetime

class SMSXMLParser:
    """Parser for extracting SMS transactions from XML file"""
    
    def __init__(self, xml_file_path="modified_sms_v2.xml"):
        self.xml_file_path = xml_file_path
        self.transactions = []
        
    def parse_xml_file(self):
        """Parse the XML file and extract all SMS transactions"""
        try:
            with open(self.xml_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print(f"Loaded XML file ({len(content)} characters)")
            return self._extract_transactions_from_xml(content)
        except FileNotFoundError:
            print(f"XML file not found. Using sample data.")
            return []
        except Exception as e:
            print(f"Error: {e}. Using sample data.")
            return []
    
    def _extract_transactions_from_xml(self, xml_content):
        """Extract transactions using regex patterns"""
        transactions = []
        
        # Regex pattern to match SMS elements
        sms_pattern = r'<sms[^>]*date="(\d+)"[^>]*body="([^"]*)"[^>]*readable_date="([^"]*)"[^>]*/>'
        
        # Find all SMS elements
        sms_matches = re.findall(sms_pattern, xml_content)
        
        for date_str, body, readable_date in sms_matches:
            try:
                # Convert timestamp to datetime
                timestamp = int(date_str) / 1000  # Convert from milliseconds
                transaction_date = datetime.fromtimestamp(timestamp).isoformat()
                
                # Parse the SMS body to extract transaction details
                parsed_transaction = self._parse_sms_body(body, transaction_date, readable_date)
                
                if parsed_transaction:
                    transactions.append(parsed_transaction)
                    
            except (ValueError, TypeError) as e:
                continue
        
        print(f"Parsed {len(transactions)} transactions from {len(sms_matches)} SMS messages")
        return transactions
    
    def _parse_sms_body(self, body, transaction_date, readable_date):
        """Parse SMS body to extract transaction information"""
        # Clean the body text
        body = body.replace('&lt;', '<').replace('&gt;', '>')
        
        # Generate deterministic ID based on SMS content
        import hashlib
        content_hash = hashlib.md5(body.encode('utf-8')).hexdigest()[:12]
        transaction_id = f"txn_{content_hash}"
        
        # Initialize transaction data
        transaction_data = {
            'transaction_id': transaction_id,
            'transaction_date': transaction_date,
            'readable_date': readable_date,
            'raw_sms': body,
            'status': 'Completed'
        }
        
        # Pattern 1: Money received (You have received X RWF from Y)
        received_pattern = r'You have received ([\d,]+) RWF from ([^(]+) \(([^)]+)\) on your mobile money account at ([^.]+)\. Message from sender: ([^.]+)\. Your new balance:([\d,]+) RWF\. Financial Transaction Id: (\d+)\.'
        match = re.search(received_pattern, body)
        if match:
            amount, sender, phone, date_time, message, balance, txn_id = match.groups()
            transaction_data.update({
                'sender_name': sender.strip(),
                'receiver_name': 'Account Holder',
                'amount': float(amount.replace(',', '')),
                'fee': 0.0,
                'balance_after': float(balance.replace(',', '')),
                'transaction_type': 'Money Received',
                'remarks': f"Received from {sender.strip()}",
                'external_transaction_id': txn_id
            })
            return transaction_data
        
        # Pattern 2: Payment completed (TxId: X. Your payment of Y RWF to Z)
        payment_pattern = r'TxId: (\d+)\. Your payment of ([\d,]+) RWF to ([^(]+) \d+ has been completed at ([^.]+)\. Your new balance: ([\d,]+) RWF\. Fee was ([\d,]+) RWF\.'
        match = re.search(payment_pattern, body)
        if match:
            txn_id, amount, receiver, date_time, balance, fee = match.groups()
            transaction_data.update({
                'sender_name': 'Account Holder',
                'receiver_name': receiver.strip(),
                'amount': float(amount.replace(',', '')),
                'fee': float(fee.replace(',', '')),
                'balance_after': float(balance.replace(',', '')),
                'transaction_type': 'Payment',
                'remarks': f"Payment to {receiver.strip()}",
                'external_transaction_id': txn_id
            })
            return transaction_data
        
        # Pattern 3: Bank deposit (*113*R*A bank deposit of X RWF)
        bank_deposit_pattern = r'\*113\*R\*A bank deposit of ([\d,]+) RWF has been added to your mobile money account at ([^.]+)\. Your NEW BALANCE :([\d,]+) RWF\.'
        match = re.search(bank_deposit_pattern, body)
        if match:
            amount, date_time, balance = match.groups()
            transaction_data.update({
                'sender_name': 'Bank',
                'receiver_name': 'Account Holder',
                'amount': float(amount.replace(',', '')),
                'fee': 0.0,
                'balance_after': float(balance.replace(',', '')),
                'transaction_type': 'Bank Deposit',
                'remarks': 'Bank deposit via cash'
            })
            return transaction_data
        
        # Pattern 4: Transfer (*165*S*X RWF transferred to Y)
        transfer_pattern = r'\*165\*S\*([\d,]+) RWF transferred to ([^(]+) \(([^)]+)\) from \d+ at ([^.]+) \. Fee was: ([\d,]+) RWF\. New balance: ([\d,]+) RWF\.'
        match = re.search(transfer_pattern, body)
        if match:
            amount, receiver, phone, date_time, fee, balance = match.groups()
            transaction_data.update({
                'sender_name': 'Account Holder',
                'receiver_name': receiver.strip(),
                'amount': float(amount.replace(',', '')),
                'fee': float(fee.replace(',', '')),
                'balance_after': float(balance.replace(',', '')),
                'transaction_type': 'Transfer',
                'remarks': f"Transfer to {receiver.strip()}"
            })
            return transaction_data
        
        # Pattern 5: Airtime purchase (*162*TxId:X*S*Your payment of Y RWF to Airtime)
        airtime_pattern = r'\*162\*TxId:(\d+)\*S\*Your payment of ([\d,]+) RWF to Airtime with token[^.]*has been completed at ([^.]+)\. Fee was ([\d,]+) RWF\. Your new balance: ([\d,]+) RWF'
        match = re.search(airtime_pattern, body)
        if match:
            txn_id, amount, date_time, fee, balance = match.groups()
            transaction_data.update({
                'sender_name': 'Account Holder',
                'receiver_name': 'Airtime Service',
                'amount': float(amount.replace(',', '')),
                'fee': float(fee.replace(',', '')),
                'balance_after': float(balance.replace(',', '')),
                'transaction_type': 'Airtime Purchase',
                'remarks': 'Airtime top-up',
                'external_transaction_id': txn_id
            })
            return transaction_data
        
        # Pattern 6: Cash withdrawal (You X have via agent: Agent Y)
        withdrawal_pattern = r'You ([^(]+) \(([^)]+)\) have via agent: Agent ([^(]+) \(([^)]+)\), withdrawn ([\d,]+) RWF from your mobile money account: \d+ at ([^.]+) and you can now collect your money in cash\. Your new balance: ([\d,]+) RWF\. Fee paid: ([\d,]+) RWF\. Message from agent: ([^.]+)\. Financial Transaction Id: (\d+)\.'
        match = re.search(withdrawal_pattern, body)
        if match:
            account_holder, account_phone, agent_name, agent_phone, amount, date_time, balance, fee, message, txn_id = match.groups()
            transaction_data.update({
                'sender_name': 'Account Holder',
                'receiver_name': f'Agent {agent_name.strip()}',
                'amount': float(amount.replace(',', '')),
                'fee': float(fee.replace(',', '')),
                'balance_after': float(balance.replace(',', '')),
                'transaction_type': 'Cash Withdrawal',
                'remarks': f"Cash withdrawal via agent {agent_name.strip()}",
                'external_transaction_id': txn_id
            })
            return transaction_data
        
        # Pattern 7: Merchant payment (*164*S*Y'ello,A transaction of X RWF by Y)
        merchant_pattern = r'\*164\*S\*Y\'ello,A transaction of ([\d,]+) RWF by ([^on]+) on your MOMO account was successfully completed at ([^.]+)\. Message from debit receiver: ([^.]+)\. Your new balance:([\d,]+) RWF\. Fee was ([\d,]+) RWF\. Financial Transaction Id: (\d+)\. External Transaction Id: ([^.]+)\.'
        match = re.search(merchant_pattern, body)
        if match:
            amount, merchant, date_time, message, balance, fee, txn_id, external_id = match.groups()
            transaction_data.update({
                'sender_name': 'Account Holder',
                'receiver_name': merchant.strip(),
                'amount': float(amount.replace(',', '')),
                'fee': float(fee.replace(',', '')),
                'balance_after': float(balance.replace(',', '')),
                'transaction_type': 'Merchant Payment',
                'remarks': f"Payment to {merchant.strip()}",
                'external_transaction_id': txn_id
            })
            return transaction_data
        
        # If no pattern matches, return None (skip this SMS)
        return None
