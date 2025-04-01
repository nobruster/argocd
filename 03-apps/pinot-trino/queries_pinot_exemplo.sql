-- Query 1: Users and Orders (Joins users with their orders)
SELECT 
    users.user_id,
    users.first_name AS user_first_name,
    users.last_name AS user_last_name,
    users.country AS user_country,
    orders.order_id,
    orders.total_amount,
    orders.order_date
FROM 
    users
JOIN 
    orders 
ON 
    users.user_id = orders.user_key;



-- Query 2: Drivers and Orders (Joins drivers with their orders)
SELECT
    drivers.driver_id,
    drivers.first_name AS driver_first_name,
    drivers.last_name AS driver_last_name,
    orders.order_id,
    orders.total_amount,
    orders.order_date
FROM 
    drivers
JOIN 
    orders
ON 
    drivers.driver_id = orders.driver_key;



-- Query 3: Orders and Drivers
SELECT
    orders.order_id,
    orders.total_amount,
    orders.order_date,
    drivers.driver_id,
    drivers.first_name AS driver_first_name,
    drivers.last_name AS driver_last_name
FROM 
    orders
JOIN 
    drivers
ON 
    drivers.driver_id = orders.driver_key;



-- Query 4: Total Orders per User
SELECT 
    users.user_id,
    users.first_name AS user_first_name,
    users.last_name AS user_last_name,
    COUNT(orders.order_id) AS total_orders,
    SUM(CAST(orders.total_amount AS DOUBLE)) AS total_spent
FROM 
    users
JOIN 
    orders 
ON 
    users.user_id = orders.user_key
GROUP BY 
    users.user_id, users.first_name, users.last_name;



-- Query 5: Total Orders per Driver
SELECT 
    drivers.driver_id,
    drivers.first_name AS driver_first_name,
    drivers.last_name AS driver_last_name,
    COUNT(orders.order_id) AS total_orders,
    SUM(CAST(orders.total_amount AS DOUBLE)) AS total_earned
FROM 
    drivers
JOIN 
    orders 
ON 
    drivers.driver_id = orders.driver_key
GROUP BY 
    drivers.driver_id, drivers.first_name, drivers.last_name;



-- Query 6: Users with No Orders
SELECT 
    users.user_id,
    users.first_name AS user_first_name,
    users.last_name AS user_last_name
FROM 
    users
LEFT JOIN 
    orders 
ON 
    users.user_id = orders.user_key
WHERE 
    orders.order_id IS NULL;



-- Query 7: Orders and Drivers (No restaurant data available)
SELECT
    orders.order_id,
    orders.total_amount,
    orders.order_date,
    drivers.driver_id,
    drivers.first_name AS driver_first_name,
    drivers.last_name AS driver_last_name
FROM 
    orders
JOIN 
    drivers
ON 
    drivers.driver_id = orders.driver_key;




-- Query 8: Orders Made by Users from a Specific Country
SELECT 
    users.user_id,
    users.first_name AS user_first_name,
    users.last_name AS user_last_name,
    orders.order_id,
    orders.total_amount,
    orders.order_date
FROM 
    users
JOIN 
    orders 
ON 
    users.user_id = orders.user_key
WHERE 
    users.country = '"BR"';  -- Replace 'Brazil' with your country of choice




-- Query 9: Drivers with the Most Orders
SELECT 
    drivers.driver_id,
    drivers.first_name AS driver_first_name,
    drivers.last_name AS driver_last_name,
    COUNT(orders.order_id) AS total_orders
FROM 
    drivers
JOIN 
    orders 
ON 
    drivers.driver_id = orders.driver_key
GROUP BY 
    drivers.driver_id, drivers.first_name, drivers.last_name
ORDER BY 
    total_orders DESC;



-- Query 10: Users with Orders Over a Specific Amount
SELECT 
    users.user_id,
    users.first_name AS user_first_name,
    users.last_name AS user_last_name,
    orders.order_id,
    orders.total_amount,
    orders.order_date
FROM 
    users
JOIN 
    orders 
ON 
    users.user_id = orders.user_key
WHERE 
    CAST(orders.total_amount AS DOUBLE) > 100.00;  -- Replace '100.00' with your desired amount



-- Query 11: Orders Made in a Date Range
SELECT 
    users.user_id,
    users.first_name AS user_first_name,
    users.last_name AS user_last_name,
    orders.order_id,
    orders.total_amount,
    orders.order_date
FROM 
    users
JOIN 
    orders 
ON 
    users.user_id = orders.user_key
WHERE 
    orders.order_date BETWEEN '2023-01-01' AND '2023-12-31';  -- Replace with your desired date range



