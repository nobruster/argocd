# querie 1

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
        users.user_id = orders.user_key


# querie 2

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
        drivers.driver_id = orders.driver_key


# querie 3

SELECT
    restaurants.restaurant_id,
    restaurants.name AS restaurant_name,
    restaurants.city AS restaurant_city,
    restaurants.country AS restaurant_country,
    restaurants.average_rating,
    ratings.rating,
    orders.order_id 
FROM restaurants
    JOIN 
        ratings 
    ON 
        restaurants.restaurant_id = ratings.restaurant_identifier
    JOIN 
        orders
    ON 
        orders.restaurant_key = restaurants.restaurant_id 



# querie final

SELECT
    uo.user_id,
    uo.user_first_name,
    uo.user_last_name,
    uo.user_country,
    d.driver_id,
    d.driver_first_name,
    d.driver_last_name,
    r.restaurant_id,
    r.restaurant_name,
    r.restaurant_city,
    r.restaurant_country,
    r.average_rating,
    r.rating,
    o.order_id,
    o.total_amount,
    o.order_date
FROM 
    (
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
            users.user_id = orders.user_key
    ) uo
JOIN 
    (
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
            drivers.driver_id = orders.driver_key
    ) d
ON uo.order_id = d.order_id
JOIN 
    (
        SELECT
            restaurants.restaurant_id,
            restaurants.name AS restaurant_name,
            restaurants.city AS restaurant_city,
            restaurants.country AS restaurant_country,
            restaurants.average_rating,
            ratings.rating,
            orders.order_id 
        FROM restaurants
        JOIN 
            ratings 
        ON 
            restaurants.restaurant_id = ratings.restaurant_identifier
        JOIN 
            orders
        ON 
            orders.restaurant_key = restaurants.restaurant_id
    ) r
ON uo.order_id = r.order_id
JOIN 
    orders o
ON uo.order_id = o.order_id;

