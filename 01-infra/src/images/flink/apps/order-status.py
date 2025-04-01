from pyflink.table import TableEnvironment, EnvironmentSettings

def simple_kafka_reader():
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(environment_settings=env_settings)

    # Configure memory settings explicitly:
    config = t_env.get_config().get_configuration()
    config.set_string("taskmanager.memory.process.size", "4g")
    config.set_string("jobmanager.memory.process.size", "2g")

    # Add Kafka Connector JAR (stable version)
    config.set_string(
        "pipeline.jars",
        "file:///Users/mateusoliveira/Mateus/owshq/GitHub/trn-mst-bdk-2-0/03-apps/flink/jars/flink-sql-connector-kafka-3.2.0-1.19.jar"
    )

    # Kafka source aligned exactly to your data
    t_env.execute_sql("""
    CREATE TABLE mongodb_status (
        status_id BIGINT,
        order_identifier STRING,
        status STRING,
        dt_current_timestamp TIMESTAMP(3),
        WATERMARK FOR dt_current_timestamp AS dt_current_timestamp - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'mongodb_status',
        'properties.bootstrap.servers' = 'localhost:9094',
        'properties.group.id' = 'simple-reader',
        'value.format' = 'json',
        'scan.startup.mode' = 'earliest-offset'
    )
    """)

    # Create print sink aligned with source
    t_env.execute_sql("""
    CREATE TABLE print_sink (
      status_id BIGINT,
      order_identifier STRING,
      status STRING,
      dt_current_timestamp TIMESTAMP(3)
    ) WITH (
      'connector' = 'print'
    )
    """)

    # Insert into print sink
    t_env.execute_sql("""
    INSERT INTO print_sink
    SELECT status_id, order_identifier, status, dt_current_timestamp
    FROM mongodb_status
    """)

    print("Flink Kafka reader is running... Press Ctrl+C to stop.")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Job terminated by user.")

if __name__ == "__main__":
    simple_kafka_reader()