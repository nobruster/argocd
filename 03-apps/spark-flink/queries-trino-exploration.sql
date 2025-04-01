-- Exibir Todos os Usuários
SELECT * 
FROM iceberg.default.users;



-- Contagem de Usuários por País
SELECT country, COUNT(*) AS total_users
FROM iceberg.default.users
GROUP BY country
ORDER BY total_users DESC;



-- Exibir Restaurantes por Cidade
SELECT restaurant_id, name, cuisine_type, average_rating, city, address
FROM iceberg.default.restaurants
WHERE city = 'São Paulo';  -- Altere para a cidade desejada



-- Média de Avaliações dos Restaurantes
SELECT restaurant_id, name, AVG(rating) AS avg_rating
FROM iceberg.default.ratings
JOIN iceberg.default.restaurants
    ON ratings.restaurant_identifier = restaurants.restaurant_id
GROUP BY restaurant_id, name
ORDER BY avg_rating DESC;




-- Detalhes dos Pedidos de um Usuário
SELECT order_id, restaurant_key, total_amount, order_date
FROM iceberg.default.orders
WHERE user_key = 12;  -- Substitua pelo `user_key` desejado




-- Exibir Status de Pedidos
SELECT order_identifier, status, status_timestamp
FROM iceberg.default.order_status
WHERE status_timestamp = (SELECT MAX(status_timestamp) 
                           FROM iceberg.default.order_status 
                           WHERE order_identifier = order_status.order_identifier)
ORDER BY status_timestamp DESC;




-- Contagem de Pedidos por Restaurante
SELECT restaurant_key, COUNT(*) AS total_orders
FROM iceberg.default.orders
GROUP BY restaurant_key
ORDER BY total_orders DESC;




-- Contagem de Pedidos por Restaurante
SELECT restaurant_key, COUNT(*) AS total_orders
FROM iceberg.default.orders
GROUP BY restaurant_key
ORDER BY total_orders DESC;




-- Detalhes de Avaliações com Restaurantes
SELECT r.restaurant_id, r.name, rt.rating, rt.timestamp
FROM iceberg.default.ratings rt
JOIN iceberg.default.restaurants r
    ON rt.restaurant_identifier = r.restaurant_id
ORDER BY rt.timestamp DESC;





-- Exibir Detalhes de Motoristas
SELECT driver_id, first_name, last_name, city, vehicle_make, vehicle_model, vehicle_license_plate
FROM iceberg.default.drivers
WHERE city = 'Rio de Janeiro';  -- Substitua pela cidade desejada




-- Verificar Pedidos Recentes
SELECT order_id, user_key, restaurant_key, total_amount, order_date
FROM iceberg.default.orders
ORDER BY order_date DESC
LIMIT 10;




-- Relação entre Pedidos e Avaliações
SELECT o.order_id, o.user_key, o.restaurant_key, r.rating, r.timestamp
FROM iceberg.default.orders o
JOIN iceberg.default.ratings r 
    ON o.restaurant_key = r.restaurant_identifier
WHERE o.order_date = r.timestamp
ORDER BY o.order_date DESC;




-- Motoristas que Dirigem Veículos de Certos Modelos
SELECT driver_id, first_name, last_name, vehicle_make, vehicle_model, vehicle_license_plate
FROM iceberg.default.drivers
WHERE vehicle_model = 'Civic';  -- Substitua pelo modelo desejado




-- Contagem de Usuários por País e Por Janela de 5 Minutos
SELECT 
    country, 
    COUNT(*) OVER (
        PARTITION BY country, 
        date_trunc('minute', CAST(dt_current_timestamp AS timestamp)) - (EXTRACT(MINUTE FROM CAST(dt_current_timestamp AS timestamp)) % 5) * INTERVAL '1' MINUTE
        ORDER BY dt_current_timestamp
    ) AS total_users_5min,
    dt_current_timestamp
FROM iceberg.default.users;




-- Média de Avaliações dos Restaurantes por Janela de 5 Minutos
SELECT 
    restaurant_id, 
    name, 
    AVG(rating) OVER (
        PARTITION BY restaurant_id,
        date_trunc('minute', CAST(timestamp AS timestamp)) - (EXTRACT(MINUTE FROM CAST(timestamp AS timestamp)) % 5) * INTERVAL '1' MINUTE
        ORDER BY timestamp
    ) AS avg_rating_5min,
    timestamp
FROM iceberg.default.ratings
JOIN iceberg.default.restaurants
    ON ratings.restaurant_identifier = restaurants.restaurant_id;





-- Média de Gastos dos Usuários por Janela de 5 Minutos
SELECT 
    o.user_key, 
    u.first_name, 
    u.last_name, 
    AVG(o.total_amount) OVER (
        PARTITION BY o.user_key,
        date_trunc('minute', CAST(o.order_date AS timestamp)) - (EXTRACT(MINUTE FROM CAST(o.order_date AS timestamp)) % 5) * INTERVAL '1' MINUTE
        ORDER BY o.order_date
    ) AS avg_spent_5min,
    o.order_date
FROM iceberg.default.orders o
JOIN iceberg.default.users u
    ON o.user_key = u.user_id
ORDER BY avg_spent_5min DESC;




-- Contagem de Pedidos por Usuário e Status por Janela de 5 Minutos
SELECT 
    o.user_key, 
    u.first_name, 
    u.last_name, 
    os.status, 
    COUNT(*) OVER (
        PARTITION BY o.user_key, os.status,
        date_trunc('minute', CAST(os.status_timestamp AS timestamp)) - (EXTRACT(MINUTE FROM CAST(os.status_timestamp AS timestamp)) % 5) * INTERVAL '1' MINUTE
        ORDER BY os.status_timestamp
    ) AS total_orders_5min,
    os.status_timestamp
FROM iceberg.default.orders o
JOIN iceberg.default.order_status os
    ON o.order_id = os.order_identifier
JOIN iceberg.default.users u
    ON o.user_key = u.user_id
ORDER BY total_orders_5min DESC;




-- Exibir Restaurantes por Cidade com Avaliação Média em Janelas de 5 Minutos
SELECT 
    r.restaurant_id, 
    r.name, 
    r.city, 
    AVG(rt.rating) OVER (
        PARTITION BY r.restaurant_id,
        date_trunc('minute', CAST(rt.timestamp AS timestamp)) - INTERVAL '1' MINUTE * (EXTRACT(MINUTE FROM CAST(rt.timestamp AS timestamp)) % 5)
        ORDER BY rt.timestamp
    ) AS avg_rating_5min,
    rt.timestamp
FROM iceberg.default.restaurants r
JOIN iceberg.default.ratings rt
    ON r.restaurant_id = rt.restaurant_identifier
WHERE r.city = 'São Paulo';  


    
    

-- Consulta para unir as tabelas de pedidos, restaurantes, motoristas, usuários e status de pedidos
-- Join entre essas tabelas e calcular algumas métricas de interesse, como:
--     Avaliação média de restaurantes por cidade.
--     Detalhes de pedidos, com status, valor total e informações do motorista.
SELECT 
    u.first_name AS user_first_name,
    u.last_name AS user_last_name,
    u.country AS user_country,
    r.name AS restaurant_name,
    r.city AS restaurant_city,
    r.average_rating AS restaurant_avg_rating,
    r.cuisine_type AS restaurant_cuisine_type,
    o.order_id,
    o.total_amount AS order_total_amount,
    CAST(o.order_date AS timestamp) AS order_date,
    os.status AS order_status,
    d.first_name AS driver_first_name,
    d.last_name AS driver_last_name,
    d.city AS driver_city,
    d.vehicle_make,
    d.vehicle_model,
    d.vehicle_license_plate,
    AVG(rt.rating) OVER (
        PARTITION BY r.restaurant_id, 
        date_trunc('minute', CAST(rt.timestamp AS timestamp)) - INTERVAL '1' MINUTE * (EXTRACT(MINUTE FROM CAST(rt.timestamp AS timestamp)) % 5)
        ORDER BY rt.timestamp
    ) AS avg_rating_5min
FROM iceberg.default.orders o
JOIN iceberg.default.users u
    ON o.user_key = u.user_id  -- Unindo usuários a pedidos
JOIN iceberg.default.restaurants r
    ON o.restaurant_key = r.restaurant_id  -- Unindo pedidos a restaurantes
JOIN iceberg.default.drivers d
    ON o.driver_key = d.driver_id  -- Unindo pedidos a motoristas
JOIN iceberg.default.ratings rt
    ON r.restaurant_id = rt.restaurant_identifier  -- Unindo restaurantes a avaliações
JOIN iceberg.default.order_status os
    ON o.order_id = os.order_identifier  -- Unindo pedidos a status de pedidos
WHERE CAST(o.order_date AS timestamp) >= TIMESTAMP '2025-03-01 00:00:00'  -- Filtro correto com timestamp
ORDER BY o.order_date DESC;




-- Consulta com JOINs e Janelas Temporais (5 minutos)
SELECT 
    u.first_name AS user_first_name,
    u.last_name AS user_last_name,
    u.country AS user_country,
    r.name AS restaurant_name,
    r.city AS restaurant_city,
    r.average_rating AS restaurant_avg_rating,
    r.cuisine_type AS restaurant_cuisine_type,
    o.order_id,
    o.total_amount AS order_total_amount,
    -- Conversão de order_date para timestamp e filtro correto
    CAST(o.order_date AS timestamp) AS order_date,
    os.status AS order_status,
    d.first_name AS driver_first_name,
    d.last_name AS driver_last_name,
    d.city AS driver_city,
    d.vehicle_make,
    d.vehicle_model,
    d.vehicle_license_plate,
    -- Média das avaliações de restaurantes por janela de 5 minutos
    AVG(rt.rating) OVER (
        PARTITION BY r.restaurant_id, 
        date_trunc('minute', CAST(rt.timestamp AS timestamp)) - INTERVAL '1' MINUTE * (EXTRACT(MINUTE FROM CAST(rt.timestamp AS timestamp)) % 5)
        ORDER BY rt.timestamp
    ) AS avg_rating_5min,
    -- Número de avaliações por janela de 5 minutos
    COUNT(rt.rating) OVER (
        PARTITION BY r.restaurant_id, 
        date_trunc('minute', CAST(rt.timestamp AS timestamp)) - INTERVAL '1' MINUTE * (EXTRACT(MINUTE FROM CAST(rt.timestamp AS timestamp)) % 5)
        ORDER BY rt.timestamp
    ) AS total_ratings_5min,
    -- Status do pedido por janela temporal
    FIRST_VALUE(os.status) OVER (
        PARTITION BY o.order_id 
        ORDER BY CAST(os.status_timestamp AS timestamp) ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_status_of_order
FROM iceberg.default.orders o
JOIN iceberg.default.users u
    ON o.user_key = u.user_id  -- Unindo usuários aos pedidos
JOIN iceberg.default.restaurants r
    ON o.restaurant_key = r.restaurant_id  -- Unindo pedidos a restaurantes
JOIN iceberg.default.drivers d
    ON o.driver_key = d.driver_id  -- Unindo pedidos a motoristas
JOIN iceberg.default.ratings rt
    ON r.restaurant_id = rt.restaurant_identifier  -- Unindo restaurantes a avaliações
JOIN iceberg.default.order_status os
    ON o.order_id = os.order_identifier  -- Unindo pedidos a status de pedidos
WHERE CAST(o.order_date AS timestamp) >= TIMESTAMP '2025-03-01 00:00:00'  -- Filtro de pedidos a partir de 1º de março de 2025
ORDER BY o.order_date DESC;


