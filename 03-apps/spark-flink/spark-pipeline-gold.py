from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, current_timestamp, sum, count
from pyspark.sql.window import Window

# Inicializando a SparkSession
spark = SparkSession.builder \
    .appName("UberEats Gold Processing") \
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

def create_table_if_not_exists(table_name, schema, location):
    query = f"""
        CREATE TABLE IF NOT EXISTS iceberg.default.{table_name} (
            {schema}
        )
        USING iceberg
        LOCATION '{location}'
    """
    spark.sql(query)

# Criando tabela Gold
create_table_if_not_exists("ubereats_gold_user_orders", """
    user_id BIGINT,
    first_name STRING,
    last_name STRING,
    cpf STRING,
    phone_number STRING,
    job STRING,
    company_name STRING,
    country STRING,
    birthday DATE,
    order_id BIGINT,
    restaurant_id BIGINT,
    driver_id BIGINT,
    order_date DATE,
    total_amount DOUBLE,
    payment_id STRING,
    order_timestamp TIMESTAMP,
    total_spent DOUBLE,
    orders_count INT
""", "s3a://lakehouse/ubereats/gold/user_orders")

# Transferindo dados para o Gold
try:
    users_silver_df = spark.read.table("iceberg.default.ubereats_silver_users")
    orders_silver_df = spark.read.table("iceberg.default.ubereats_silver_orders")

    window_spec = Window.partitionBy("user_id")
    
    gold_df = users_silver_df.join(orders_silver_df, "user_id") \
        .select(
            users_silver_df["user_id"],
            users_silver_df["first_name"],
            users_silver_df["last_name"],
            users_silver_df["cpf"],
            users_silver_df["phone_number"],
            users_silver_df["job"],
            users_silver_df["company_name"],
            users_silver_df["country"],
            users_silver_df["birthday"],
            orders_silver_df["order_id"],
            orders_silver_df["restaurant_id"],
            orders_silver_df["driver_id"],
            orders_silver_df["order_date"],
            orders_silver_df["total_amount"],
            orders_silver_df["payment_id"],
            orders_silver_df["dt_current_timestamp"].alias("order_timestamp"),
            sum("total_amount").over(window_spec).alias("total_spent"),
            count("order_id").over(window_spec).alias("orders_count")
        )

    gold_df.write.mode("append").format("iceberg").saveAsTable("iceberg.default.ubereats_gold_user_orders")
    print("Dados de pedidos e usuários transferidos para o Gold com sucesso!")
except Exception as e:
    print(f"Erro ao transferir dados para o Gold: {str(e)}")

# Finalizando a SparkSession
spark.stop()