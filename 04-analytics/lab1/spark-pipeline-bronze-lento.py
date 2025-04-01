import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, expr

# Inicializando a SparkSession
spark = SparkSession.builder \
    .appName("Cell Tower Processing") \
    .config("spark.hive.metastore.uris", "thrift://hive-metastore.deepstore.svc.cluster.local:9083") \
    .config("fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.iceberg", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.iceberg.type", "hive") \
    .config("spark.sql.catalog.iceberg.warehouse", "s3a://warehouse") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://datalake-hl.deepstore.svc.cluster.local:9000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

log4j = spark._jvm.org.apache.log4j
logger = log4j.LogManager.getLogger("PySparkIceberg")

def create_table_if_not_exists(table_name, schema, location):
    query = f"""
        CREATE TABLE IF NOT EXISTS iceberg.default.{table_name} (
            {schema}
        )
        USING iceberg
        LOCATION '{location}'
    """
    spark.sql(query)

# Criando tabelas Bronze
create_table_if_not_exists("ubereats_bronze_users", """
    user_id BIGINT,
    country STRING,
    birthday STRING,
    job STRING,
    phone_number STRING,
    uuid STRING,
    last_name STRING,
    first_name STRING,
    cpf STRING,
    company_name STRING,
    dt_current_timestamp STRING
""", "s3a://lakehouse/ubereats/bronze/users")

create_table_if_not_exists("ubereats_bronze_orders", """
    order_id BIGINT,
    user_key BIGINT,
    restaurant_key BIGINT,
    driver_key BIGINT,
    order_date STRING,
    total_amount DOUBLE,
    payment_id STRING,
    dt_current_timestamp STRING
""", "s3a://lakehouse/ubereats/bronze/orders")

create_table_if_not_exists("ubereats_bronze_restaurants", """
    country STRING,
    city STRING,
    restaurant_id BIGINT,
    phone_number STRING,
    cnpj STRING,
    average_rating DOUBLE,
    name STRING,
    uuid STRING,
    address STRING,
    opening_time STRING,
    cuisine_type STRING,
    closing_time STRING,
    num_reviews DOUBLE,
    dt_current_timestamp STRING
""", "s3a://lakehouse/ubereats/bronze/restaurants")

create_table_if_not_exists("ubereats_bronze_ratings", """
    rating_id BIGINT,
    uuid STRING,
    restaurant_identifier BIGINT,
    rating DOUBLE,
    timestamp STRING,
    dt_current_timestamp STRING
""", "s3a://lakehouse/ubereats/bronze/ratings")

# Função para simular delay no processamento
def simulate_delay(seconds=5):
    logger.info(f"Simulando delay de {seconds} segundos...")
    time.sleep(seconds)

# Transferindo dados para o Bronze
try:
    users_df = spark.read.table("iceberg.default.users")
    filtered_users_df = users_df.filter(col("dt_current_timestamp").cast("timestamp") >= current_timestamp() - expr("INTERVAL 5 MINUTES"))
    simulate_delay(120)  # Delay de 120 segundos
    filtered_users_df.write.mode("append").format("iceberg").saveAsTable("iceberg.default.ubereats_bronze_users")
    logger.info("Dados de usuários transferidos com sucesso!")
except Exception as e:
    logger.error(f"Erro ao transferir dados de usuários: {str(e)}")

try:
    orders_df = spark.read.table("iceberg.default.orders")
    filtered_orders_df = orders_df.filter(col("dt_current_timestamp").cast("timestamp") >= current_timestamp() - expr("INTERVAL 5 MINUTES"))
    simulate_delay(120)  # Delay de 120 segundos
    filtered_orders_df.write.mode("append").format("iceberg").saveAsTable("iceberg.default.ubereats_bronze_orders")
    logger.info("Dados de pedidos transferidos com sucesso!")
except Exception as e:
    logger.error(f"Erro ao transferir dados de pedidos: {str(e)}")

try:
    restaurants_df = spark.read.table("iceberg.default.restaurants")
    filtered_restaurants_df = restaurants_df.filter(col("dt_current_timestamp").cast("timestamp") >= current_timestamp() - expr("INTERVAL 5 MINUTES"))
    simulate_delay(120)  # Delay de 120 segundos
    filtered_restaurants_df.write.mode("append").format("iceberg").saveAsTable("iceberg.default.ubereats_bronze_restaurants")
    logger.info("Dados de restaurantes transferidos com sucesso!")
except Exception as e:
    logger.error(f"Erro ao transferir dados de restaurantes: {str(e)}")

try:
    ratings_df = spark.read.table("iceberg.default.ratings")
    filtered_ratings_df = ratings_df.filter(col("dt_current_timestamp").cast("timestamp") >= current_timestamp() - expr("INTERVAL 5 MINUTES"))
    simulate_delay(120)  # Delay de 120 segundos
    filtered_ratings_df.write.mode("append").format("iceberg").saveAsTable("iceberg.default.ubereats_bronze_ratings")
    logger.info("Dados de avaliações transferidos com sucesso!")
except Exception as e:
    logger.error(f"Erro ao transferir dados de avaliações: {str(e)}")

# Finalizando a SparkSession
spark.stop()
