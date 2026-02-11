-- CREATE TABLE IF NOT EXISTS insurance_claims (
--     claim_id INTEGER,
--     policy_id INTEGER,
--     customer_id INTEGER,
--     claim_date DATE,
--     claim_amount FLOAT,
--     claim_status TEXT,   -- APPROVED / REJECTED / PENDING
--     processing_days INTEGER
-- );

-- DELETE FROM insurance_claims;

-- INSERT INTO insurance_claims VALUES
-- -- Normal baseline period
-- (1, 101, 1001, '2024-01-01', 12000, 'APPROVED', 7),
-- (2, 102, 1002, '2024-01-01', 8000,  'APPROVED', 5),
-- (3, 103, 1003, '2024-01-02', 15000, 'APPROVED', 8),
-- (4, 104, 1004, '2024-01-02', 9000,  'REJECTED', 4),
-- (5, 105, 1005, '2024-01-03', 11000, 'APPROVED', 6),
-- (6, 106, 1006, '2024-01-03', 13000, 'APPROVED', 7),
-- (7, 107, 1007, '2024-01-04', 10000, 'APPROVED', 6),
-- (8, 108, 1008, '2024-01-04', 9500,  'REJECTED', 5),
-- (9, 109, 1009, '2024-01-05', 12500, 'APPROVED', 7),
-- (10,110, 1010, '2024-01-05', 10500, 'APPROVED', 6);




INSERT INTO insurance_claims VALUES
(99, 999, 1999, '2024-01-06', 200000, 'APPROVED', 2);


-- Triggers:

-- Daily Claim Amount 🚨

-- Avg Claim Amount 🚨



-- INSERT INTO insurance_claims VALUES
-- (100, 1000, 2000, '2024-01-06', 9000, 'REJECTED', 3),
-- (101, 1001, 2001, '2024-01-06', 8500, 'REJECTED', 4),
-- (102, 1002, 2002, '2024-01-06', 7800, 'REJECTED', 3);


-- Triggers:

-- Approval Rate 🚨



-- INSERT INTO insurance_claims VALUES
-- (103, 1003, 2003, '2024-01-06', 10000, 'APPROVED', 25);


-- Triggers:

-- Avg Processing Time 🚨


-- INSERT INTO insurance_claims VALUES
-- (104, 1004, 2004, '2024-01-07', 18000, 'APPROVED', 7);


-- Triggers:

-- Avg Claim Amount ⚠️ (gradual drift)



-- data injest ground level
-- azure push(daily refresh)
-- data engineer - madelian architechture 
-- broze layer- as it is
-- silver layer - 
-- gold layer - 
-- BI developer 
-- data scientists 


-- actual money , excel money ,BI money
