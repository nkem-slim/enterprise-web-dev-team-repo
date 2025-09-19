-- Sample Data for MoMo SMS Database
-- Insert test data for all tables

USE momo_sms_db;

-- Insert Transaction Categories
INSERT INTO Transaction_Categories (category_name, description) VALUES
('Deposit', 'Money deposited into account'),
('Withdrawal', 'Money withdrawn from account'),
('Transfer', 'Money transferred between accounts'),
('Payment', 'Payment for goods or services'),
('Airtime', 'Mobile airtime purchase'),
('Bill Payment', 'Utility bill payments'),
('Cash Out', 'Cash withdrawal from agent'),
('Cash In', 'Cash deposit through agent');

-- Insert Users
INSERT INTO Users (full_name, phone_number, role, created_at) VALUES
('Jane Smith', '250791666666', 'Customer', '2024-05-10 16:30:51'),
('Samuel Carter', '250790777777', 'Customer', '2024-05-10 21:32:32'),
('Alex Doe', '250788999999', 'Customer', '2024-05-12 20:49:30'),
('Robert Brown', '250789888888', 'Customer', '2024-05-14 09:11:32'),
('Agent Sophia', '250790777777', 'Agent', '2024-05-26 02:10:27'),
('Merchant Store', '250790000000', 'Merchant', '2024-05-15 10:00:00'),
('System Admin', NULL, 'System', '2024-05-01 00:00:00'),
('Agent Michael', '250790111111', 'Agent', '2024-05-20 14:30:00');

-- Insert Transactions
INSERT INTO Transactions (transaction_id, sender_id, receiver_id, category_id, amount, fee, balance_after, transaction_date, channel, status, remarks) VALUES
(1001, 1, 2, 3, 5000.00, 25.00, 49500.00, '2024-05-15 10:30:00', 'SMS', 'Completed', 'Transfer to Samuel'),
(1002, 2, 1, 3, 2000.00, 10.00, 47500.00, '2024-05-15 11:15:00', 'SMS', 'Completed', 'Transfer back to Jane'),
(1003, 1, 5, 1, 10000.00, 50.00, 37500.00, '2024-05-15 12:00:00', 'SMS', 'Completed', 'Deposit through agent'),
(1004, 2, 6, 4, 1500.00, 7.50, 46000.00, '2024-05-15 13:30:00', 'SMS', 'Completed', 'Payment to merchant'),
(1005, 1, 1, 5, 500.00, 2.50, 37000.00, '2024-05-15 14:00:00', 'SMS', 'Completed', 'Airtime purchase'),
(1006, 3, 4, 3, 3000.00, 15.00, 47000.00, '2024-05-15 15:00:00', 'SMS', 'Completed', 'Transfer to Robert'),
(1007, 4, 3, 3, 1000.00, 5.00, 46000.00, '2024-05-15 16:00:00', 'SMS', 'Completed', 'Transfer back to Alex'),
(1008, 2, 5, 1, 5000.00, 25.00, 41000.00, '2024-05-15 17:00:00', 'SMS', 'Completed', 'Deposit through agent'),
(1009, 1, 2, 3, 2500.00, 12.50, 34500.00, '2024-05-15 18:00:00', 'SMS', 'Failed', 'Insufficient balance'),
(1010, 3, 6, 4, 800.00, 4.00, 45200.00, '2024-05-15 19:00:00', 'SMS', 'Completed', 'Payment to merchant');

-- Insert System Logs
INSERT INTO System_Logs (transaction_id, raw_sms, parsed_status, notes) VALUES
(1001, 'You have received 5000.00 from Jane Smith. New balance: 49500.00. Ref: TXN1001', 'Parsed', 'Successfully parsed transfer transaction'),
(1002, 'You have sent 2000.00 to Jane Smith. New balance: 47500.00. Ref: TXN1002', 'Parsed', 'Successfully parsed transfer transaction'),
(1003, 'Deposit of 10000.00 successful. New balance: 37500.00. Ref: TXN1003', 'Parsed', 'Successfully parsed deposit transaction'),
(1004, 'Payment of 1500.00 to Merchant Store successful. New balance: 46000.00. Ref: TXN1004', 'Parsed', 'Successfully parsed payment transaction'),
(1005, 'Airtime purchase of 500.00 successful. New balance: 37000.00. Ref: TXN1005', 'Parsed', 'Successfully parsed airtime transaction'),
(1006, 'You have received 3000.00 from Alex Doe. New balance: 47000.00. Ref: TXN1006', 'Parsed', 'Successfully parsed transfer transaction'),
(1007, 'You have sent 1000.00 to Alex Doe. New balance: 46000.00. Ref: TXN1007', 'Parsed', 'Successfully parsed transfer transaction'),
(1008, 'Deposit of 5000.00 successful. New balance: 41000.00. Ref: TXN1008', 'Parsed', 'Successfully parsed deposit transaction'),
(1009, 'Transfer failed: Insufficient balance. Ref: TXN1009', 'Error', 'Failed to parse due to insufficient balance'),
(1010, 'Payment of 800.00 to Merchant Store successful. New balance: 45200.00. Ref: TXN1010', 'Parsed', 'Successfully parsed payment transaction');
