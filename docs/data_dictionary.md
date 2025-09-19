# Data Dictionary

## Sample Data Dictionary

### Users Table Sample Data

| user_id | full_name     | phone_number | role     | created_at          |
| ------- | ------------- | ------------ | -------- | ------------------- |
| 1       | Jane Smith    | 250791666666 | Customer | 2024-05-10 16:30:51 |
| 2       | Samuel Carter | 250790777777 | Customer | 2024-05-10 21:32:32 |
| 3       | Alex Doe      | 250788999999 | Customer | 2024-05-12 20:49:30 |
| 4       | Robert Brown  | 250789888888 | Customer | 2024-05-14 09:11:32 |
| 5       | Agent Sophia  | 250790777777 | Agent    | 2024-05-26 02:10:27 |

### Transaction Categories Sample Data

| category_id | category_name | description                        |
| ----------- | ------------- | ---------------------------------- |
| 1           | Deposit       | Money deposited into account       |
| 2           | Withdrawal    | Money withdrawn from account       |
| 3           | Transfer      | Money transferred between accounts |
| 4           | Payment       | Payment for goods or services      |
| 5           | Airtime       | Mobile airtime purchase            |
| 6           | Bill Payment  | Utility bill payments              |
| 7           | Cash Out      | Cash withdrawal from agent         |
| 8           | Cash In       | Cash deposit through agent         |

### Transactions Sample Data

| transaction_id | sender_id | receiver_id | category_id | amount   | fee   | balance_after | transaction_date    | channel | status    | remarks               |
| -------------- | --------- | ----------- | ----------- | -------- | ----- | ------------- | ------------------- | ------- | --------- | --------------------- |
| 1001           | 1         | 2           | 3           | 5000.00  | 25.00 | 49500.00      | 2024-05-15 10:30:00 | SMS     | Completed | Transfer to Samuel    |
| 1002           | 2         | 1           | 3           | 2000.00  | 10.00 | 47500.00      | 2024-05-15 11:15:00 | SMS     | Completed | Transfer back to Jane |
| 1003           | 1         | 5           | 1           | 10000.00 | 50.00 | 37500.00      | 2024-05-15 12:00:00 | SMS     | Completed | Deposit through agent |
| 1004           | 2         | 6           | 4           | 1500.00  | 7.50  | 46000.00      | 2024-05-15 13:30:00 | SMS     | Completed | Payment to merchant   |
| 1005           | 1         | 1           | 5           | 500.00   | 2.50  | 37000.00      | 2024-05-15 14:00:00 | SMS     | Completed | Airtime purchase      |
| 1006           | 3         | 4           | 3           | 3000.00  | 15.00 | 47000.00      | 2024-05-15 15:00:00 | SMS     | Completed | Transfer to Robert    |
| 1007           | 4         | 3           | 3           | 1000.00  | 5.00  | 46000.00      | 2024-05-15 16:00:00 | SMS     | Completed | Transfer back to Alex |
| 1008           | 2         | 5           | 1           | 5000.00  | 25.00 | 41000.00      | 2024-05-15 17:00:00 | SMS     | Completed | Deposit through agent |
| 1009           | 1         | 2           | 3           | 2500.00  | 12.50 | 34500.00      | 2024-05-15 18:00:00 | SMS     | Failed    | Insufficient balance  |
| 1010           | 3         | 6           | 4           | 800.00   | 4.00  | 45200.00      | 2024-05-15 19:00:00 | SMS     | Completed | Payment to merchant   |

### System Logs Sample Data

| log_id | transaction_id | raw_sms                                                                              | parsed_status | created_at          | notes                                       |
| ------ | -------------- | ------------------------------------------------------------------------------------ | ------------- | ------------------- | ------------------------------------------- |
| 1      | 1001           | You have received 5000.00 from Jane Smith. New balance: 49500.00. Ref: TXN1001       | Parsed        | 2024-05-15 10:30:00 | Successfully parsed transfer transaction    |
| 2      | 1002           | You have sent 2000.00 to Jane Smith. New balance: 47500.00. Ref: TXN1002             | Parsed        | 2024-05-15 11:15:00 | Successfully parsed transfer transaction    |
| 3      | 1003           | Deposit of 10000.00 successful. New balance: 37500.00. Ref: TXN1003                  | Parsed        | 2024-05-15 12:00:00 | Successfully parsed deposit transaction     |
| 4      | 1004           | Payment of 1500.00 to Merchant Store successful. New balance: 46000.00. Ref: TXN1004 | Parsed        | 2024-05-15 13:30:00 | Successfully parsed payment transaction     |
| 5      | 1005           | Airtime purchase of 500.00 successful. New balance: 37000.00. Ref: TXN1005           | Parsed        | 2024-05-15 14:00:00 | Successfully parsed airtime transaction     |
| 6      | 1006           | You have received 3000.00 from Alex Doe. New balance: 47000.00. Ref: TXN1006         | Parsed        | 2024-05-15 15:00:00 | Successfully parsed transfer transaction    |
| 7      | 1007           | You have sent 1000.00 to Alex Doe. New balance: 46000.00. Ref: TXN1007               | Parsed        | 2024-05-15 16:00:00 | Successfully parsed transfer transaction    |
| 8      | 1008           | Deposit of 5000.00 successful. New balance: 41000.00. Ref: TXN1008                   | Parsed        | 2024-05-15 17:00:00 | Successfully parsed deposit transaction     |
| 9      | 1009           | Transfer failed: Insufficient balance. Ref: TXN1009                                  | Error         | 2024-05-15 18:00:00 | Failed to parse due to insufficient balance |
| 10     | 1010           | Payment of 800.00 to Merchant Store successful. New balance: 45200.00. Ref: TXN1010  | Parsed        | 2024-05-15 19:00:00 | Successfully parsed payment transaction     |

## Field Descriptions

### Users Table Fields

- **user_id**: Unique identifier for each user (Primary Key)
- **full_name**: Complete name of the user
- **phone_number**: Mobile phone number in international format (250XXXXXXXXX)
- **role**: User type (Customer, Agent, Merchant, System)
- **created_at**: Timestamp when user account was created

### Transactions Table Fields

- **transaction_id**: Unique identifier for each transaction (Primary Key)
- **sender_id**: User ID of the person sending money (Foreign Key to Users)
- **receiver_id**: User ID of the person receiving money (Foreign Key to Users)
- **category_id**: Type of transaction (Foreign Key to Transaction_Categories)
- **amount**: Transaction amount in local currency
- **fee**: Service fee charged for the transaction
- **balance_after**: Account balance after transaction completion
- **transaction_date**: When the transaction occurred
- **channel**: How the transaction was initiated (SMS, USSD, App, etc.)
- **status**: Transaction outcome (Completed, Failed, Pending)
- **remarks**: Additional notes about the transaction

### Transaction_Categories Table Fields

- **category_id**: Unique identifier for each category (Primary Key)
- **category_name**: Name of the transaction type
- **description**: Detailed explanation of the category

### System_Logs Table Fields

- **log_id**: Unique identifier for each log entry (Primary Key)
- **transaction_id**: Associated transaction ID (Foreign Key to Transactions)
- **raw_sms**: Original SMS message received
- **parsed_status**: Whether SMS was successfully parsed (Parsed, Error, Pending)
- **created_at**: When the log entry was created
- **notes**: Additional information about the parsing process

## Data Relationships

### Primary Relationships

1. **Users → Transactions**: One user can have many transactions (as sender or receiver)
2. **Transaction_Categories → Transactions**: One category can have many transactions
3. **Transactions → System_Logs**: One transaction can have one system log entry

### Business Rules

1. **Phone Number Format**: Must be 12 digits starting with 250 (Rwanda country code)
2. **Transaction Amounts**: Must be positive values
3. **Fees**: Must be non-negative values
4. **Balances**: Must be non-negative values
5. **Transaction Status**: Must be one of the defined ENUM values
6. **User Roles**: Must be one of the defined ENUM values
