import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, current_timestamp, sum, count, expr
from pyspark.sql.window import Window

# Inicializando a SparkSession
spark = SparkSession.builder \
    .appName("UberEats Silver Processing") \
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

# Criando tabelas Silver
create_table_if_not_exists("ubereats_silver_users", """
    user_id BIGINT,
    country STRING,
    birthday DATE,
    job STRING,
    phone_number STRING,
    uuid STRING,
    last_name STRING,
    first_name STRING,
    cpf STRING,
    company_name STRING,
    dt_current_timestamp TIMESTAMP
""", "s3a://lakehouse/ubereats/silver/users")

create_table_if_not_exists("ubereats_silver_orders", """
    order_id BIGINT,
    user_id BIGINT,
    restaurant_id BIGINT,
    driver_id BIGINT,
    order_date DATE,
    total_amount DOUBLE,
    payment_id STRING,
    dt_current_timestamp TIMESTAMP
""", "s3a://lakehouse/ubereats/silver/orders")


# Função para simular delay no processamento
def simulate_delay(seconds=5):
    logger.info(f"Simulando delay de {seconds} segundos...")
    time.sleep(seconds)

# Transferindo dados para o Silver
try:
    users_bronze_df = spark.read.table("iceberg.default.ubereats_bronze_users")
    users_silver_df = users_bronze_df.select(
        col("user_id"),
        col("country"),
        to_date(col("birthday")).alias("birthday"),
        col("job"),
        col("phone_number"),
        col("uuid"),
        col("last_name"),
        col("first_name"),
        col("cpf"),
        col("company_name"),
        col("dt_current_timestamp").cast("timestamp").alias("dt_current_timestamp")
    )
    users_silver_df.write.mode("append").format("iceberg").saveAsTable("iceberg.default.ubereats_silver_users")
    simulate_delay(120)  # Delay de 120 segundos
    print("Dados de usuários transferidos com sucesso!")
except Exception as e:
    print(f"Erro ao transferir dados de usuários: {str(e)}")

try:
    orders_bronze_df = spark.read.table("iceberg.default.ubereats_bronze_orders")
    orders_silver_df = orders_bronze_df.select(
        col("order_id"),
        col("user_key").alias("user_id"),
        col("restaurant_key").alias("restaurant_id"),
        col("driver_key").alias("driver_id"),
        to_date(col("order_date")).alias("order_date"),
        col("total_amount"),
        col("payment_id"),
        col("dt_current_timestamp").cast("timestamp").alias("dt_current_timestamp")
    )
    orders_silver_df.write.mode("append").format("iceberg").saveAsTable("iceberg.default.ubereats_silver_orders")
    simulate_delay(120)  # Delay de 120 segundos
    print("Dados de pedidos transferidos com sucesso!")
except Exception as e:
    print(f"Erro ao transferir dados de pedidos: {str(e)}")

# Finalizando a SparkSession
spark.stop()
