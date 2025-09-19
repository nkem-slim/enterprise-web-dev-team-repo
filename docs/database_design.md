# Database Design Documentation

## Overview

This document describes the database design for the MoMo SMS Data Processing System, including the Entity Relationship Diagram (ERD), table structures, and design rationale.

## Entity Relationship Diagram

[ERD diagram should be placed here - docs/erd_diagram.png]

## Design Rationale

### Core Entities

1. **Users**: Central entity storing all user types (customers, agents, merchants, system)
2. **Transactions**: Main financial transaction records with full audit trail
3. **Transaction_Categories**: Lookup table for transaction types
4. **System_Logs**: Audit trail for SMS parsing and processing

### Key Design Decisions

#### 1. User Management

- **Single Users table**: Consolidates all user types (customers, agents, merchants) into one table
- **Role-based access**: Uses ENUM for role definition with clear business rules
- **Phone number validation**: CHECK constraint ensures valid phone number format
- **Flexible identification**: Allows NULL phone numbers for system users

#### 2. Transaction Processing

- **BigInt transaction_id**: Ensures scalability for high-volume transactions
- **Decimal precision**: 12,2 precision for amounts supports large transactions with cent accuracy
- **Referential integrity**: Foreign keys maintain data consistency
- **Status tracking**: ENUM for transaction status with clear business states

#### 3. Data Integrity

- **CHECK constraints**: Validate amount ranges, phone number formats
- **Foreign key constraints**: Maintain referential integrity
- **Unique constraints**: Prevent duplicate phone numbers and category names
- **Cascade deletes**: Appropriate cleanup when parent records are deleted

#### 4. Performance Optimization

- **Strategic indexing**: Indexes on frequently queried columns
- **Composite indexes**: For complex query patterns
- **View creation**: Pre-computed joins for common queries
- **Stored procedures**: Encapsulate complex business logic

## Data Dictionary

### Users Table

| Column       | Type         | Constraints                 | Description                                   |
| ------------ | ------------ | --------------------------- | --------------------------------------------- |
| user_id      | INT          | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier                        |
| full_name    | VARCHAR(100) | NOT NULL                    | User's full name                              |
| phone_number | VARCHAR(20)  | UNIQUE, CHECK constraint    | User's phone number                           |
| role         | ENUM         | DEFAULT 'Customer'          | User role (Customer, Agent, Merchant, System) |
| created_at   | DATETIME     | DEFAULT CURRENT_TIMESTAMP   | Account creation timestamp                    |

### Transactions Table

| Column           | Type          | Constraints           | Description                       |
| ---------------- | ------------- | --------------------- | --------------------------------- |
| transaction_id   | BIGINT        | PRIMARY KEY           | Unique transaction identifier     |
| sender_id        | INT           | FOREIGN KEY           | Sender user ID                    |
| receiver_id      | INT           | FOREIGN KEY           | Receiver user ID                  |
| category_id      | INT           | FOREIGN KEY, NOT NULL | Transaction category ID           |
| amount           | DECIMAL(12,2) | NOT NULL, CHECK > 0   | Transaction amount                |
| fee              | DECIMAL(12,2) | DEFAULT 0, CHECK >= 0 | Transaction fee                   |
| balance_after    | DECIMAL(12,2) | CHECK >= 0            | Account balance after transaction |
| transaction_date | DATETIME      | NOT NULL              | Transaction timestamp             |
| channel          | VARCHAR(50)   | DEFAULT 'SMS'         | Transaction channel               |
| status           | ENUM          | DEFAULT 'Completed'   | Transaction status                |
| remarks          | TEXT          |                       | Additional transaction notes      |

### Transaction_Categories Table

| Column        | Type        | Constraints                 | Description                |
| ------------- | ----------- | --------------------------- | -------------------------- |
| category_id   | INT         | PRIMARY KEY, AUTO_INCREMENT | Unique category identifier |
| category_name | VARCHAR(50) | NOT NULL, UNIQUE            | Category name              |
| description   | TEXT        |                             | Category description       |

### System_Logs Table

| Column         | Type     | Constraints                 | Description               |
| -------------- | -------- | --------------------------- | ------------------------- |
| log_id         | INT      | PRIMARY KEY, AUTO_INCREMENT | Unique log identifier     |
| transaction_id | BIGINT   | FOREIGN KEY                 | Associated transaction ID |
| raw_sms        | TEXT     | NOT NULL                    | Original SMS message      |
| parsed_status  | ENUM     | DEFAULT 'Parsed'            | Parsing status            |
| created_at     | DATETIME | DEFAULT CURRENT_TIMESTAMP   | Log creation timestamp    |
| notes          | TEXT     |                             | Additional parsing notes  |

## Security and Accuracy Enhancements

### 1. Data Validation Rules

- **Phone number format**: Regex validation for 9-12 digit numbers
- **Amount validation**: Positive amounts only
- **Fee validation**: Non-negative fees
- **Balance validation**: Non-negative balances

### 2. Referential Integrity

- **Cascade deletes**: Categories can be deleted, users set to NULL
- **Foreign key constraints**: Prevent orphaned records
- **Unique constraints**: Prevent duplicate phone numbers

### 3. Audit Trail

- **System logs**: Complete SMS parsing history
- **Transaction tracking**: Full transaction lifecycle
- **Status monitoring**: Parsing success/failure tracking

## Sample Queries

### 1. Daily Transaction Summary

```sql
SELECT
    DATE(transaction_date) as date,
    COUNT(*) as total_transactions,
    SUM(amount) as total_amount,
    SUM(fee) as total_fees
FROM Transactions
GROUP BY DATE(transaction_date)
ORDER BY date DESC;
```

### 2. User Transaction History

```sql
SELECT
    t.transaction_id,
    t.amount,
    t.transaction_date,
    t.status,
    c.category_name
FROM Transactions t
JOIN Users u ON (t.sender_id = u.user_id OR t.receiver_id = u.user_id)
JOIN Transaction_Categories c ON t.category_id = c.category_id
WHERE u.phone_number = '08012345678'
ORDER BY t.transaction_date DESC;
```

### 3. Failed Transaction Analysis

```sql
SELECT
    t.transaction_id,
    t.amount,
    t.transaction_date,
    sl.raw_sms,
    sl.notes
FROM Transactions t
JOIN System_Logs sl ON t.transaction_id = sl.transaction_id
WHERE t.status = 'Failed';
```

## Performance Considerations

### Indexes

- **Primary indexes**: All primary keys
- **Foreign key indexes**: All foreign key columns
- **Query optimization indexes**: Date, status, phone number
- **Composite indexes**: For complex query patterns

### Views

- **Transaction_Summary**: Pre-computed joins for common queries
- **User_Transaction_History**: Optimized user transaction retrieval

### Stored Procedures

- **GetUserTransactionHistory**: Encapsulated user query logic
- **GetDailyTransactionSummary**: Optimized daily reporting

## Future Scalability

### Horizontal Scaling

- **Partitioning**: By transaction date for large datasets
- **Sharding**: By user_id for distributed processing
- **Read replicas**: For reporting and analytics

### Vertical Scaling

- **Index optimization**: Regular index maintenance
- **Query optimization**: Continuous performance monitoring
- **Storage optimization**: Archive old transaction data
