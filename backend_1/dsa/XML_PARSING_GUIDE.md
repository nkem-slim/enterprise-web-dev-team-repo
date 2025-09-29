# XML Parsing Guide

## Overview

The SMS Transactions REST API now includes comprehensive XML parsing functionality that automatically extracts transaction data from SMS backup XML files using advanced regex patterns.

## Regex Patterns Implemented

### 1. Money Received Pattern

```regex
You have received ([\d,]+) RWF from ([^(]+) \(([^)]+)\) on your mobile money account at ([^.]+)\. Message from sender: ([^.]+)\. Your new balance:([\d,]+) RWF\. Financial Transaction Id: (\d+)\.
```

**Extracts:**

- Amount received
- Sender name
- Sender phone (masked)
- Transaction date/time
- Sender message
- New balance
- Financial transaction ID

### 2. Payment Pattern

```regex
TxId: (\d+)\. Your payment of ([\d,]+) RWF to ([^(]+) \d+ has been completed at ([^.]+)\. Your new balance: ([\d,]+) RWF\. Fee was ([\d,]+) RWF\.
```

**Extracts:**

- Transaction ID
- Payment amount
- Receiver name
- Transaction date/time
- New balance
- Fee charged

### 3. Bank Deposit Pattern

```regex
\*113\*R\*A bank deposit of ([\d,]+) RWF has been added to your mobile money account at ([^.]+)\. Your NEW BALANCE :([\d,]+) RWF\.
```

**Extracts:**

- Deposit amount
- Transaction date/time
- New balance

### 4. Transfer Pattern

```regex
\*165\*S\*([\d,]+) RWF transferred to ([^(]+) \(([^)]+)\) from \d+ at ([^.]+) \. Fee was: ([\d,]+) RWF\. New balance: ([\d,]+) RWF\.
```

**Extracts:**

- Transfer amount
- Receiver name
- Receiver phone
- Transaction date/time
- Fee charged
- New balance

### 5. Airtime Purchase Pattern

```regex
\*162\*TxId:(\d+)\*S\*Your payment of ([\d,]+) RWF to Airtime with token[^.]*has been completed at ([^.]+)\. Fee was ([\d,]+) RWF\. Your new balance: ([\d,]+) RWF
```

**Extracts:**

- Transaction ID
- Payment amount
- Transaction date/time
- Fee charged
- New balance

### 6. Cash Withdrawal Pattern

```regex
You ([^(]+) \(([^)]+)\) have via agent: Agent ([^(]+) \(([^)]+)\), withdrawn ([\d,]+) RWF from your mobile money account: \d+ at ([^.]+) and you can now collect your money in cash\. Your new balance: ([\d,]+) RWF\. Fee paid: ([\d,]+) RWF\. Message from agent: ([^.]+)\. Financial Transaction Id: (\d+)\.
```

**Extracts:**

- Account holder name
- Account holder phone
- Agent name
- Agent phone
- Withdrawal amount
- Transaction date/time
- New balance
- Fee paid
- Agent message
- Financial transaction ID

### 7. Merchant Payment Pattern

```regex
\*164\*S\*Y\'ello,A transaction of ([\d,]+) RWF by ([^on]+) on your MOMO account was successfully completed at ([^.]+)\. Message from debit receiver: ([^.]+)\. Your new balance:([\d,]+) RWF\. Fee was ([\d,]+) RWF\. Financial Transaction Id: (\d+)\. External Transaction Id: ([^.]+)\.
```

**Extracts:**

- Payment amount
- Merchant name
- Transaction date/time
- Receiver message
- New balance
- Fee charged
- Financial transaction ID
- External transaction ID

## Implementation Details

### SMSXMLParser Class

The `SMSXMLParser` class handles the XML parsing functionality:

```python
class SMSXMLParser:
    def __init__(self, xml_file_path="../modified_sms_v2.xml"):
        self.xml_file_path = xml_file_path
        self.transactions = []

    def parse_xml_file(self):
        """Parse the XML file and extract all SMS transactions"""

    def _extract_transactions_from_xml(self, xml_content):
        """Extract transactions using regex patterns"""

    def _parse_sms_body(self, body, transaction_date, readable_date):
        """Parse SMS body to extract transaction information"""
```

### Key Features

1. **Automatic XML Detection**: Looks for `../modified_sms_v2.xml` by default
2. **Fallback Mechanism**: Uses sample data if XML parsing fails
3. **Error Handling**: Graceful handling of parsing errors
4. **Pattern Matching**: 7 different regex patterns for various transaction types
5. **Data Cleaning**: Handles HTML entities and special characters
6. **Timestamp Conversion**: Converts Unix timestamps to ISO format

### Data Extraction Process

1. **XML Parsing**: Uses regex to extract SMS elements from XML
2. **Timestamp Conversion**: Converts millisecond timestamps to ISO datetime
3. **Pattern Matching**: Applies regex patterns to identify transaction types
4. **Data Structuring**: Creates standardized transaction objects
5. **Validation**: Ensures data integrity and completeness

## Usage

### Automatic Loading

The server automatically loads XML data on startup:

```python
# In TransactionStorage.__init__()
parser = SMSXMLParser()
parsed_transactions = parser.parse_xml_file()
```

### Manual Testing

Test the XML parsing functionality:

```bash
python test_xml_parser.py
```

### Custom XML File

To use a different XML file:

```python
parser = SMSXMLParser("path/to/your/sms_backup.xml")
transactions = parser.parse_xml_file()
```

## Transaction Data Structure

Each parsed transaction includes:

```python
{
    'transaction_id': 'uuid-string',
    'sender_name': 'Sender Name',
    'receiver_name': 'Receiver Name',
    'amount': 1000.00,
    'fee': 10.00,
    'balance_after': 5000.00,
    'transaction_date': '2024-05-10T16:30:51',
    'transaction_type': 'Transfer',
    'status': 'Completed',
    'remarks': 'Transaction description',
    'external_transaction_id': '123456789',
    'raw_sms': 'Original SMS text',
    'readable_date': '10 May 2024 4:30:58 PM'
}
```

## Error Handling

The parser includes comprehensive error handling:

- **File Not Found**: Falls back to sample data
- **Parsing Errors**: Logs errors and continues processing
- **Invalid Data**: Skips malformed transactions
- **Pattern Mismatch**: Returns None for unmatched patterns

## Performance Considerations

- **Memory Efficient**: Processes XML in chunks
- **Regex Optimization**: Compiled patterns for better performance
- **Error Recovery**: Continues processing even if individual transactions fail
- **Logging**: Detailed logging for debugging and monitoring

## Future Enhancements

- **Additional Patterns**: Support for more transaction types
- **Pattern Learning**: Machine learning for pattern recognition
- **Validation Rules**: Enhanced data validation
- **Batch Processing**: Support for large XML files
- **Caching**: Cache parsed data for faster startup
