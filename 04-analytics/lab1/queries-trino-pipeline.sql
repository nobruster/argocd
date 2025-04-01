


-- MEDALLION PIPELINE




-- --------------------------
--
-- TABELA - BRONZE
--
-- ---------------------------

-- Criando a tabela de usuários no Bronze
CREATE TABLE iceberg.default.ubereats_bronze_users (
   user_id bigint,
   country varchar,
   birthday varchar,
   job varchar,
   phone_number varchar,
   uuid varchar,
   last_name varchar,
   first_name varchar,
   cpf varchar,
   company_name varchar,
   dt_current_timestamp varchar
)
WITH (
   format = 'PARQUET',
   format_version = 2,
   location = 's3a://lakehouse/ubereats/bronze/users'
);

-- Criando a tabela de pedidos no Bronze
CREATE TABLE iceberg.default.ubereats_bronze_orders (
   order_id bigint,
   user_key bigint,
   restaurant_key bigint,
   driver_key bigint,
   order_date varchar,
   total_amount double,
   payment_id varchar,
   dt_current_timestamp varchar
)
WITH (
   format = 'PARQUET',
   format_version = 2,
   location = 's3a://lakehouse/ubereats/bronze/orders'
);

-- Criando a tabela de restaurantes no Bronze
CREATE TABLE iceberg.default.ubereats_bronze_restaurants (
   country varchar,
   city varchar,
   restaurant_id bigint,
   phone_number varchar,
   cnpj varchar,
   average_rating double,
   name varchar,
   uuid varchar,
   address varchar,
   opening_time varchar,
   cuisine_type varchar,
   closing_time varchar,
   num_reviews double,
   dt_current_timestamp varchar
)
WITH (
   format = 'PARQUET',
   format_version = 2,
   location = 's3a://lakehouse/ubereats/bronze/restaurants'
);

-- Criando a tabela de ratings no Bronze
CREATE TABLE iceberg.default.ubereats_bronze_ratings (
   rating_id bigint,
   uuid varchar,
   restaurant_identifier bigint,
   rating double,
   timestamp varchar,
   dt_current_timestamp varchar
)
WITH (
   format = 'PARQUET',
   format_version = 2,
   location = 's3a://lakehouse/ubereats/bronze/ratings'
);





-- --------------------------
--
-- TABELA - SILVER
--
-- ---------------------------


-- Criando a tabela de usuários no Silver (dados limpos e formatados)
CREATE TABLE iceberg.default.ubereats_silver_users (
   user_id bigint,
   country varchar,
   birthday date,  -- Convertido para data
   job varchar,
   phone_number varchar,
   uuid varchar,
   last_name varchar,
   first_name varchar,
   cpf varchar,
   company_name varchar,
   dt_current_timestamp timestamp  -- Alterado para timestamp
)
WITH (
   format = 'PARQUET',
   format_version = 2,
   location = 's3a://lakehouse/ubereats/silver/users'
);

-- Criando a tabela de pedidos no Silver (dados limpos e formatados)
CREATE TABLE iceberg.default.ubereats_silver_orders (
   order_id bigint,
   user_id bigint,  -- Renomeado para corresponder à tabela de usuários
   restaurant_id bigint,  -- Renomeado para corresponder à tabela de restaurantes
   driver_id bigint,  -- Renomeado para corresponder ao driver
   order_date date,  -- Convertido para data
   total_amount double,
   payment_id varchar,
   dt_current_timestamp timestamp  -- Alterado para timestamp
)
WITH (
   format = 'PARQUET',
   format_version = 2,
   location = 's3a://lakehouse/ubereats/silver/orders'
);





-- --------------------------
--
-- TABELA - GOLD
--
-- ---------------------------


-- Criando a tabela GOLD que integra dados de usuários e pedidos
CREATE TABLE iceberg.default.ubereats_gold_user_orders (
    user_id bigint,
    first_name varchar,
    last_name varchar,
    cpf varchar,
    phone_number varchar,
    job varchar,
    company_name varchar,
    country varchar,
    birthday date,
    order_id bigint,
    restaurant_id bigint,
    driver_id bigint,
    order_date date,
    total_amount double,
    payment_id varchar,
    order_timestamp timestamp,
    total_spent double, 
    orders_count integer  
)
WITH (
    format = 'PARQUET',
    format_version = 2,
    location = 's3a://lakehouse/ubereats/gold/user_orders'
);












-- --------------------------  ---------------------------
--
--                       PIPELINE
--
-- ---------------------------  ---------------------------




-- --------------------------
--
-- QUERIES - BRONZE
--
-- ---------------------------


-- Transferir dados de usuários para o Bronze
INSERT INTO iceberg.default.ubereats_bronze_users
SELECT 
    user_id, 
    country, 
    birthday, 
    job, 
    phone_number, 
    uuid, 
    last_name, 
    first_name, 
    cpf, 
    company_name, 
    dt_current_timestamp
FROM iceberg.default.users
WHERE CAST(dt_current_timestamp AS timestamp) >= current_timestamp - INTERVAL '5' MINUTE;


-- Transferir dados de pedidos para o Bronze
INSERT INTO iceberg.default.ubereats_bronze_orders
SELECT 
    order_id, 
    user_key, 
    restaurant_key, 
    driver_key, 
    order_date, 
    total_amount, 
    payment_id, 
    dt_current_timestamp
FROM iceberg.default.orders
WHERE CAST(dt_current_timestamp AS timestamp) >= current_timestamp - INTERVAL '5' MINUTE;


-- Transferir dados de restaurantes para o Bronze
INSERT INTO iceberg.default.ubereats_bronze_restaurants
SELECT 
    country, 
    city, 
    restaurant_id, 
    phone_number, 
    cnpj, 
    average_rating, 
    name, 
    uuid, 
    address, 
    opening_time, 
    cuisine_type, 
    closing_time, 
    num_reviews, 
    dt_current_timestamp
FROM iceberg.default.restaurants
WHERE CAST(dt_current_timestamp AS timestamp) >= current_timestamp - INTERVAL '5' MINUTE;


-- Transferir dados de ratings para o Bronze
INSERT INTO iceberg.default.ubereats_bronze_ratings
SELECT 
    rating_id, 
    uuid, 
    restaurant_identifier, 
    rating, 
    timestamp, 
    dt_current_timestamp
FROM iceberg.default.ratings
WHERE CAST(dt_current_timestamp AS timestamp) >= current_timestamp - INTERVAL '5' MINUTE;






-- --------------------------
--
-- QUERIES - SILVER
--
-- ---------------------------



-- Inserir dados na tabela de usuários no Silver
INSERT INTO iceberg.default.ubereats_silver_users
SELECT
   user_id,
   country,
   CAST(SUBSTRING(birthday, 1, 10) AS DATE) AS birthday,  
   job,
   phone_number,
   uuid,
   last_name,
   first_name,
   cpf,
   company_name,
   CAST(dt_current_timestamp AS TIMESTAMP) AS dt_current_timestamp  
FROM iceberg.default.ubereats_bronze_users;


-- Inserir dados na tabela de pedidos no Silver
INSERT INTO iceberg.default.ubereats_silver_orders
SELECT
   order_id,
   user_key AS user_id,  
   restaurant_key AS restaurant_id,  
   driver_key AS driver_id,  
   CAST(SUBSTRING(order_date, 1, 10) AS DATE) AS order_date,  
   total_amount,
   payment_id,
   CAST(dt_current_timestamp AS TIMESTAMP) AS dt_current_timestamp  
FROM iceberg.default.ubereats_bronze_orders;





-- --------------------------
--
-- QUERIES - GOLD
--
-- ---------------------------

-- Inserindo dados na tabela GOLD, unindo informações de usuários e pedidos
INSERT INTO iceberg.default.ubereats_gold_user_orders
SELECT
    u.user_id,
    u.first_name,
    u.last_name,
    u.cpf,
    u.phone_number,
    u.job,
    u.company_name,
    u.country,
    u.birthday,
    o.order_id,
    o.restaurant_id,
    o.driver_id,
    o.order_date,
    o.total_amount,
    o.payment_id,
    o.dt_current_timestamp AS order_timestamp,
    SUM(o.total_amount) OVER (PARTITION BY u.user_id) AS total_spent,
    COUNT(o.order_id) OVER (PARTITION BY u.user_id) AS orders_count
FROM iceberg.default.ubereats_silver_users u
JOIN iceberg.default.ubereats_silver_orders o
    ON u.user_id = o.user_id;









-- Remover a tabela de usuários no Silver
DROP TABLE IF EXISTS iceberg.default.ubereats_silver_users;

-- Remover a tabela de pedidos no Silver
DROP TABLE IF EXISTS iceberg.default.ubereats_silver_orders;

-- Remover a tabela de restaurantes no Silver
DROP TABLE IF EXISTS iceberg.default.ubereats_silver_restaurants;

-- Remover a tabela de ratings no Silver
DROP TABLE IF EXISTS iceberg.default.ubereats_silver_ratings;
