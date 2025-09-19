-- CRUD Operations and Test Queries for MoMo SMS Database
-- Demonstrates database functionality

USE momo_sms_db;

-- =============================================
-- CREATE OPERATIONS (INSERT)
-- =============================================

-- Insert new user
INSERT INTO Users (full_name, phone_number, role) 
VALUES ('Test User', '08099999999', 'Customer');

-- Insert new transaction category
INSERT INTO Transaction_Categories (category_name, description) 
VALUES ('Test Category', 'Test description for new category');

-- Insert new transaction
INSERT INTO Transactions (transaction_id, sender_id, receiver_id, category_id, amount, fee, balance_after, transaction_date, channel, status, remarks) 
VALUES (1011, 1, 2, 3, 1000.00, 5.00, 34000.00, NOW(), 'SMS', 'Completed', 'Test transaction');

-- =============================================
-- READ OPERATIONS (SELECT)
-- =============================================

-- 1. Get all transactions with user details
SELECT 
    t.transaction_id,
    t.amount,
    t.fee,
    t.transaction_date,
    t.status,
    s.full_name as sender_name,
    r.full_name as receiver_name,
    c.category_name
FROM Transactions t
LEFT JOIN Users s ON t.sender_id = s.user_id
LEFT JOIN Users r ON t.receiver_id = r.user_id
LEFT JOIN Transaction_Categories c ON t.category_id = c.category_id
ORDER BY t.transaction_date DESC;

-- 2. Get transaction summary by category
SELECT 
    c.category_name,
    COUNT(*) as transaction_count,
    SUM(t.amount) as total_amount,
    AVG(t.amount) as average_amount,
    SUM(t.fee) as total_fees
FROM Transactions t
JOIN Transaction_Categories c ON t.category_id = c.category_id
GROUP BY c.category_id, c.category_name
ORDER BY total_amount DESC;

-- 3. Get daily transaction summary
SELECT 
    DATE(transaction_date) as date,
    COUNT(*) as total_transactions,
    SUM(amount) as total_amount,
    SUM(fee) as total_fees,
    COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_count,
    COUNT(CASE WHEN status = 'Failed' THEN 1 END) as failed_count
FROM Transactions
GROUP BY DATE(transaction_date)
ORDER BY date DESC;

-- 4. Get user transaction history
SELECT 
    t.transaction_id,
    t.amount,
    t.fee,
    t.transaction_date,
    t.status,
    CASE 
        WHEN t.sender_id = u.user_id THEN 'Sent'
        WHEN t.receiver_id = u.user_id THEN 'Received'
    END as transaction_type,
    c.category_name
FROM Transactions t
JOIN Users u ON (t.sender_id = u.user_id OR t.receiver_id = u.user_id)
JOIN Transaction_Categories c ON t.category_id = c.category_id
WHERE u.phone_number = '250791666666'
ORDER BY t.transaction_date DESC;

-- 5. Get failed transactions with details
SELECT 
    t.transaction_id,
    t.amount,
    t.transaction_date,
    s.full_name as sender_name,
    r.full_name as receiver_name,
    c.category_name,
    sl.raw_sms,
    sl.notes
FROM Transactions t
LEFT JOIN Users s ON t.sender_id = s.user_id
LEFT JOIN Users r ON t.receiver_id = r.user_id
LEFT JOIN Transaction_Categories c ON t.category_id = c.category_id
LEFT JOIN System_Logs sl ON t.transaction_id = sl.transaction_id
WHERE t.status = 'Failed';

-- =============================================
-- UPDATE OPERATIONS
-- =============================================

-- Update user information
UPDATE Users 
SET full_name = 'John Updated Doe' 
WHERE user_id = 1;

-- Update transaction status
UPDATE Transactions 
SET status = 'Completed', remarks = 'Updated status' 
WHERE transaction_id = 1009;

-- Update system log
UPDATE System_Logs 
SET parsed_status = 'Parsed', notes = 'Updated after manual review' 
WHERE log_id = 9;

-- =============================================
-- DELETE OPERATIONS
-- =============================================

-- Delete test user (safe delete due to foreign key constraints)
DELETE FROM Users WHERE phone_number = '08099999999';

-- Delete test transaction category (safe delete due to foreign key constraints)
DELETE FROM Transaction_Categories WHERE category_name = 'Test Category';

-- =============================================
-- COMPLEX QUERIES
-- =============================================

-- 1. Top 5 users by transaction volume
SELECT 
    u.full_name,
    u.phone_number,
    COUNT(t.transaction_id) as transaction_count,
    SUM(t.amount) as total_amount,
    SUM(t.fee) as total_fees
FROM Users u
JOIN Transactions t ON (u.user_id = t.sender_id OR u.user_id = t.receiver_id)
GROUP BY u.user_id, u.full_name, u.phone_number
ORDER BY total_amount DESC
LIMIT 5;

-- 2. Monthly transaction trends
SELECT 
    YEAR(transaction_date) as year,
    MONTH(transaction_date) as month,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount
FROM Transactions
WHERE status = 'Completed'
GROUP BY YEAR(transaction_date), MONTH(transaction_date)
ORDER BY year DESC, month DESC;

-- 3. Agent performance analysis
SELECT 
    u.full_name as agent_name,
    u.phone_number,
    COUNT(t.transaction_id) as transactions_processed,
    SUM(t.amount) as total_amount_processed,
    SUM(t.fee) as total_fees_collected
FROM Users u
JOIN Transactions t ON (u.user_id = t.sender_id OR u.user_id = t.receiver_id)
WHERE u.role = 'Agent'
GROUP BY u.user_id, u.full_name, u.phone_number
ORDER BY total_amount_processed DESC;

-- 4. System health check
SELECT 
    'Total Users' as metric,
    COUNT(*) as value
FROM Users
UNION ALL
SELECT 
    'Total Transactions',
    COUNT(*)
FROM Transactions
UNION ALL
SELECT 
    'Completed Transactions',
    COUNT(*)
FROM Transactions
WHERE status = 'Completed'
UNION ALL
SELECT 
    'Failed Transactions',
    COUNT(*)
FROM Transactions
WHERE status = 'Failed'
UNION ALL
SELECT 
    'Parsed Logs',
    COUNT(*)
FROM System_Logs
WHERE parsed_status = 'Parsed'
UNION ALL
SELECT 
    'Error Logs',
    COUNT(*)
FROM System_Logs
WHERE parsed_status = 'Error';


