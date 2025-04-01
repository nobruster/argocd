

from pyflink.table import TableEnvironment, EnvironmentSettings


# Configuração do ambiente Flink
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(environment_settings=env_settings)



# --------------------------------------
##
## QUERIES NA TABELA USERS - select to watch the messages flow
##
# --------------------------------------

# SQL para criar a tabela Kafka com o schema fornecido
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
        'scan.startup.mode' = 'latest-offset'  
    )
""")




# A simple select in all columns in the table
table_result = t_env.execute_sql("""
    SELECT * FROM user_data
""")

with table_result.collect() as results:
    for row in results:
        print(row)




# Showing the number of people by country
table_result = t_env.execute_sql("""
    SELECT country, COUNT(*) AS user_count
    FROM user_data
    GROUP BY country
""")

with table_result.collect() as results:
    for row in results:
        print(row)




# Filtrando usuarios com CPF valido
table_result = t_env.execute_sql("""
    SELECT * 
    FROM user_data
    WHERE cpf LIKE '___.___.___-__'  
""")

with table_result.collect() as results:
    for row in results:
        print(row)





# Filtrando usuarios pelo nome
table_result = t_env.execute_sql("""
    SELECT * 
    FROM user_data
    WHERE first_name LIKE 'Maria%'
""")

with table_result.collect() as results:
    for row in results:
        print(row)








# ===========================================================================================

from pyflink.table import TableEnvironment, EnvironmentSettings


# Configuração do ambiente Flink
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(environment_settings=env_settings)



# --------------------------------------
##
## QUERIES NA TABELA DRIVERS - select to watch the messages flow
##
# --------------------------------------

# SQL para criar a tabela Kafka com o schema fornecido
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
        'scan.startup.mode' = 'latest-offset'  
    )
""")


# A simple select in all columns in the table
table_result = t_env.execute_sql("""
    SELECT * FROM driver_data
""")


# Showing the query result
with table_result.collect() as results:
    for row in results:
        print(row)




# Motoristas por paises
table_result = t_env.execute_sql("""
    SELECT country, COUNT(*) AS driver_count
    FROM driver_data
    GROUP BY country
""")

with table_result.collect() as results:
    for row in results:
        print(row)




# Motoristas de cidades especificas
table_result = t_env.execute_sql("""
    SELECT * 
    FROM driver_data
    WHERE city = 'São Paulo'
""")

with table_result.collect() as results:
    for row in results:
        print(row)


# checking
table_result = t_env.execute_sql("SHOW TABLES")

with table_result.collect() as results:
    for row in results:
        print(row)



# ===========================================================================================



# --------------------------------------
##
## QUERIES NA TABELA RESTAURANT - select to watch the messages flow
##
# --------------------------------------

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
        'scan.startup.mode' = 'latest-offset'
    )
""")


# A simple select in all columns in the table
table_result = t_env.execute_sql("""
    SELECT * FROM restaurant_data
""")


# Showing the query result
with table_result.collect() as results:
    for row in results:
        print(row)







# ===========================================================================================



# --------------------------------------
##
## QUERIES NA TABELA RATINGS - select to watch the messages flow
##
# --------------------------------------

# SQL para criar a tabela Kafka com o schema fornecido
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
        'scan.startup.mode' = 'latest-offset'
    )
""")


# A simple select in all columns in the table
table_result = t_env.execute_sql("""
    SELECT * FROM ratings_data
""")


# Showing the query result
with table_result.collect() as results:
    for row in results:
        print(row)








# ===========================================================================================



# --------------------------------------
##
## QUERIES NA TABELA ORDERS - select to watch the messages flow
##
# --------------------------------------

# SQL para criar a tabela Kafka com o schema fornecido
t_env.execute_sql("""
    CREATE TABLE orders_data (
        order_id STRING,
        user_key DOUBLE,
        restaurant_key DOUBLE,
        driver_key DOUBLE,
        order_date STRING,  -- campo original
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
        'scan.startup.mode' = 'latest-offset'
    )
""")


# A simple select in all columns in the table
table_result = t_env.execute_sql("""
    SELECT * FROM orders_data
""")


# Showing the query result
with table_result.collect() as results:
    for row in results:
        print(row)









# ===========================================================================================



# --------------------------------------
##
## QUERIES NA TABELA ORDER-STATUS - select to watch the messages flow
##
# --------------------------------------

# SQL para criar a tabela Kafka com o schema fornecido
t_env.execute_sql("""
    CREATE TABLE order_status_data (
        status_id INT,
        order_identifier INT,
        status STRING,
        status_timestamp STRING,
        dt_current_timestamp STRING
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'order-status',  
        'properties.bootstrap.servers' = 'dev-cluster-kafka-bootstrap.ingestion:9092',  
        'properties.group.id' = 'flink-group',  
        'key.format' = 'avro-confluent',  
        'key.fields' = 'status_id', 
        'key.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081', 
        'value.format' = 'avro-confluent',  
        'value.avro-confluent.url' = 'http://confluent-schema-registry-cp-schema-registry.ingestion:8081',  
        'scan.startup.mode' = 'latest-offset'
    )
""")


# A simple select in all columns in the table
table_result = t_env.execute_sql("""
    SELECT * FROM order_status_data
""")


# Showing the query result
with table_result.collect() as results:
    for row in results:
        print(row)
