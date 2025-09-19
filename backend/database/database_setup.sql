-- MoMo SMS Data Processing Database Setup
-- Created by Team Adventure

-- 1. Create Database
CREATE DATABASE IF NOT EXISTS momo_sms_db;
USE momo_sms_db;

-- 2. Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    role ENUM('Customer','Agent','Merchant','System') DEFAULT 'Customer',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_phone CHECK (phone_number REGEXP '^[0-9]{9,12}$' OR phone_number IS NULL)
) COMMENT = 'Stores customer, agent, merchant, and system users.';

-- 3. Transaction Categories
CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
) COMMENT = 'Defines types of transactions (Deposit, Payment, Transfer, etc.).';

-- 4. Transactions
CREATE TABLE Transactions (
    transaction_id BIGINT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    category_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    fee DECIMAL(12,2) DEFAULT 0,
    balance_after DECIMAL(12,2),
    transaction_date DATETIME NOT NULL,
    channel VARCHAR(50) DEFAULT 'SMS',
    status ENUM('Completed','Failed','Pending') DEFAULT 'Completed',
    remarks TEXT,
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE SET NULL,
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE SET NULL,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id) ON DELETE CASCADE
) COMMENT = 'Main financial transactions table.';

-- 5. System Logs
CREATE TABLE System_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id BIGINT,
    raw_sms TEXT NOT NULL,
    parsed_status ENUM('Parsed','Error','Pending') DEFAULT 'Parsed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id) ON DELETE SET NULL
) COMMENT = 'Stores original SMS messages and parsing logs.';

-- 6. Create Indexes for Performance
CREATE INDEX idx_transactions_date ON Transactions(transaction_date);
CREATE INDEX idx_transactions_sender ON Transactions(sender_id);
CREATE INDEX idx_transactions_receiver ON Transactions(receiver_id);
CREATE INDEX idx_transactions_category ON Transactions(category_id);
CREATE INDEX idx_transactions_status ON Transactions(status);
CREATE INDEX idx_users_phone ON Users(phone_number);
CREATE INDEX idx_users_role ON Users(role);
CREATE INDEX idx_system_logs_transaction ON System_Logs(transaction_id);
CREATE INDEX idx_system_logs_status ON System_Logs(parsed_status);

-- 7. Additional Constraints for Data Integrity
ALTER TABLE Transactions 
ADD CONSTRAINT chk_amount CHECK (amount > 0),
ADD CONSTRAINT chk_fee CHECK (fee >= 0),
ADD CONSTRAINT chk_balance CHECK (balance_after >= 0);

-- 8. Create Views for Common Queries
CREATE VIEW Transaction_Summary AS
SELECT 
    t.transaction_id,
    t.amount,
    t.fee,
    t.transaction_date,
    t.status,
    s.full_name as sender_name,
    r.full_name as receiver_name,
    c.category_name,
    c.description as category_description
FROM Transactions t
LEFT JOIN Users s ON t.sender_id = s.user_id
LEFT JOIN Users r ON t.receiver_id = r.user_id
LEFT JOIN Transaction_Categories c ON t.category_id = c.category_id;

-- 9. Create Stored Procedures
DELIMITER //

CREATE PROCEDURE GetUserTransactionHistory(IN user_phone VARCHAR(20))
BEGIN
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
    WHERE u.phone_number = user_phone
    ORDER BY t.transaction_date DESC;
END //

CREATE PROCEDURE GetDailyTransactionSummary(IN target_date DATE)
BEGIN
    SELECT 
        DATE(transaction_date) as date,
        COUNT(*) as total_transactions,
        SUM(amount) as total_amount,
        SUM(fee) as total_fees,
        COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_count,
        COUNT(CASE WHEN status = 'Failed' THEN 1 END) as failed_count
    FROM Transactions
    WHERE DATE(transaction_date) = target_date
    GROUP BY DATE(transaction_date);
END //

DELIMITER ;
