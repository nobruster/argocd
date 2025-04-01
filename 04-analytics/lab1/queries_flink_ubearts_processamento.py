from pyflink.table import TableEnvironment, EnvironmentSettings

# Configuração do ambiente Flink
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(environment_settings=env_settings)

# Criar tabelas Kafka conforme o esquema (não repetirei as declarações de criação das tabelas, pois já foram fornecidas)
# SQL para criar a tabela Kafka com o schema fornecido
t_env.execute_sql("""
    CREATE TABLE restaurant_data (
        restaurant_id BIGINT,
        name STRING,
        country STRING,
        city STRING,
        phone_number STRING,
        cnpj STRING,
        average_rating DOUBLE,
        uuid STRING,
        address STRING,
        opening_time STRING,
        cuisine_type STRING,
        closing_time STRING,
        num_reviews DOUBLE,
        dt_current_timestamp STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'restaurants',  
        'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',  
        'properties.group.id' = 'flink-group',  
        'key.format' = 'avro-confluent',  
        'key.fields' = 'restaurant_id', 
        'key.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081', 
        'value.format' = 'avro-confluent',  
        'value.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081',  
        'scan.startup.mode' = 'earliest-offset'
    )
""")



t_env.execute_sql("""
    CREATE TABLE user_data (
        birthday STRING,
        company_name STRING,
        country STRING,
        cpf STRING,
        dt_current_timestamp STRING,
        first_name STRING,
        job STRING,
        last_name STRING,
        phone_number STRING,
        user_id BIGINT,
        uuid STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'users',  
        'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',  
        'properties.group.id' = 'flink-group',  
        'key.format' = 'avro-confluent',  
        'key.fields' = 'user_id', 
        'key.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081', 
        'value.format' = 'avro-confluent',  
        'value.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081',  
        'scan.startup.mode' = 'earliest-offset'  
    )
""")


t_env.execute_sql("""
    CREATE TABLE driver_data (
        country STRING,
        date_birth STRING,
        city STRING,
        vehicle_year DOUBLE,  
        phone_number STRING,
        license_number STRING,
        vehicle_make STRING,
        uuid STRING,
        vehicle_model STRING,
        driver_id BIGINT,  
        last_name STRING,
        first_name STRING,
        vehicle_license_plate STRING,
        vehicle_type STRING,
        dt_current_timestamp STRING  
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'drivers',  
        'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',  
        'properties.group.id' = 'flink-group',  
        'key.format' = 'avro-confluent',  
        'key.fields' = 'driver_id', 
        'key.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081', 
        'value.format' = 'avro-confluent',  
        'value.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081',  
        'scan.startup.mode' = 'earliest-offset'  
    )
""")



t_env.execute_sql("""
    CREATE TABLE orders_data (
        order_id BIGINT,
        user_key DOUBLE,
        restaurant_key DOUBLE,
        driver_key DOUBLE,
        order_date STRING,
        total_amount DOUBLE,
        payment_id STRING,
        dt_current_timestamp STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'orders',  
        'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',  
        'properties.group.id' = 'flink-group',  
        'key.format' = 'avro-confluent',  
        'key.fields' = 'order_id', 
        'key.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081', 
        'value.format' = 'avro-confluent',  
        'value.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081',  
        'scan.startup.mode' = 'earliest-offset'
    )
""")




t_env.execute_sql("""
    CREATE TABLE ratings_data (
        rating_id BIGINT,
        uuid STRING,
        restaurant_identifier DOUBLE,
        rating DOUBLE,
        `timestamp` STRING,
        dt_current_timestamp STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'ratings',  
        'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',  
        'properties.group.id' = 'flink-group',  
        'key.format' = 'avro-confluent',  
        'key.fields' = 'rating_id', 
        'key.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081', 
        'value.format' = 'avro-confluent',  
        'value.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081',  
        'scan.startup.mode' = 'earliest-offset'
    )
""")



# Criar join entre as tabelas USERS e ORDERS
t_env.execute_sql("""
    CREATE VIEW user_order_data AS
    SELECT
        u.user_id,
        u.first_name AS user_first_name,
        u.last_name AS user_last_name,
        u.country AS user_country,
        o.order_id,
        o.total_amount,
        o.order_date
    FROM user_data u
    INNER JOIN orders_data o
    ON u.user_id = o.user_key
""")


# Criar join entre as tabelas DRIVERS e ORDERS
t_env.execute_sql("""
    CREATE VIEW driver_order_data AS
    SELECT
        d.driver_id,
        d.first_name AS driver_first_name,
        d.last_name AS driver_last_name,
        o.order_id,
        o.total_amount,
        o.order_date
    FROM driver_data d
    INNER JOIN orders_data o
    ON d.driver_id = o.driver_key
""")




# Criar join entre as tabelas RESTAURANTS e RATINGS
t_env.execute_sql("""
    CREATE VIEW restaurant_rating_data AS
    SELECT
        r.restaurant_id,
        r.name AS restaurant_name,
        r.city AS restaurant_city,
        r.country AS restaurant_country,
        r.average_rating,
        rt.rating,
        o.order_id 
    FROM restaurant_data r
    INNER JOIN ratings_data rt
    ON r.restaurant_id = rt.restaurant_identifier
    INNER JOIN orders_data o
    ON o.restaurant_key = r.restaurant_id 
""")





# Realizar um join completo entre as três tabelas (user, driver e restaurant)
# Criar join completo entre as três tabelas (user, driver e restaurant) e orders_data
t_env.execute_sql("""
    CREATE VIEW full_order_details AS
    SELECT
        uo.user_id,
        uo.user_first_name,
        uo.user_last_name,
        uo.user_country,
        do.driver_id,
        do.driver_first_name,
        do.driver_last_name,
        ro.restaurant_id,
        ro.restaurant_name,
        ro.restaurant_city,
        ro.restaurant_country,
        ro.average_rating,
        ro.rating,
        o.order_id,
        o.total_amount,
        o.order_date
    FROM user_order_data uo
    INNER JOIN driver_order_data do
    ON uo.order_id = do.order_id
    INNER JOIN restaurant_rating_data ro
    ON uo.order_id = ro.order_id
    INNER JOIN orders_data o 
    ON uo.order_id = o.order_id  
""")



# topico final com schema em json
# t_env.execute_sql("""
#     CREATE TABLE full_order_details_output (
#         user_id INT,
#         user_first_name STRING,
#         user_last_name STRING,
#         user_country STRING,
#         driver_id INT,
#         driver_first_name STRING,
#         driver_last_name STRING,
#         restaurant_id INT,
#         restaurant_name STRING,
#         restaurant_city STRING,
#         restaurant_country STRING,
#         average_rating FLOAT,
#         rating INT,
#         order_id INT,
#         total_amount FLOAT,
#         order_date TIMESTAMP(3)
#     ) WITH (
#         'connector' = 'kafka',
#         'topic' = 'full-order-details-topic',
#         'properties.group.id' = 'flink-group',
#         'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',
#         'format' = 'json'
#     )
# """)


# topico final com schema em avro
t_env.execute_sql("""
    CREATE TABLE full_order_details_output (
        user_id INT,
        user_first_name STRING,
        user_last_name STRING,
        user_country STRING,
        driver_id INT,
        driver_first_name STRING,
        driver_last_name STRING,
        restaurant_id INT,
        restaurant_name STRING,
        restaurant_city STRING,
        restaurant_country STRING,
        average_rating FLOAT,
        rating INT,
        order_id INT,
        total_amount FLOAT,
        order_date TIMESTAMP(3)
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'full-order-details-topic',
        'properties.group.id' = 'flink-group',
        'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',
        'key.format' = 'avro-confluent', 
        'key.fields' = 'order_id', 
        'key.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081', 
        'value.format' = 'avro-confluent',  
        'value.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081'
    )
""")




# Inserir os dados no tópico de saída
t_env.execute_sql("""
    INSERT INTO full_order_details_output
    SELECT 
        CAST(user_id AS INT) AS user_id,
        user_first_name,
        user_last_name,
        user_country,
        CAST(driver_id AS INT) AS driver_id,
        driver_first_name,
        driver_last_name,
        CAST(restaurant_id AS INT) AS restaurant_id,
        restaurant_name,
        restaurant_city,
        restaurant_country,
        CAST(average_rating AS FLOAT) AS average_rating,
        CAST(rating AS INT) AS rating,
        CAST(order_id AS INT) AS order_id,
        CAST(total_amount AS FLOAT) AS total_amount,
        CAST(order_date AS TIMESTAMP(3)) AS order_date
    FROM full_order_details
""")