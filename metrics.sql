SELECT
    DATE(order_date) AS date,
    SUM(amount) AS value
FROM orders
GROUP BY DATE(order_date);
