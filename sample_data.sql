CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER,
    order_date DATE,
    amount FLOAT
);

INSERT INTO orders VALUES
(1, '2024-01-01', 100),
(3, '2024-01-02', 150),
(5, '2024-01-03', 160),
(7, '2024-01-04', 165),
(9, '2024-01-05', 168),
(11,'2024-01-06', 169),
(13,'2024-01-07', 170);



-- DELETE FROM orders;

-- INSERT INTO orders VALUES
-- (20, '2024-01-08', 20);

-- data injest ground level
-- azure push(daily refresh)
-- data engineer - madelian architechture 
-- broze layer- as it is
-- silver layer - 
-- gold layer - 
-- BI developer 
-- data scientists 


-- actual money , excel money ,BI money
