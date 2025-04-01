from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

def main():
    # Configuração do ambiente Flink
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.in_streaming_mode()
    tenv = StreamTableEnvironment.create(env, settings)

    # Lista com os caminhos dos JARs
    jars = [
        "file:///opt/flink/lib/flink-connector-kafka-3.3.0-1.20.jar",
        "file:///opt/flink/lib/flink-sql-connector-kafka-3.3.0-1.20.jar"
    ]

    # Adicionar todos os JARs ao ambiente Flink
    for jar in jars:
        env.add_jars(jar)


    # Criar as tabelas de origem do Kafka conforme o schema fornecido

    tenv.execute_sql("""
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

    tenv.execute_sql("""
        SELECT * FROM user_data
    """)


if __name__ == "__main__":
    main()
