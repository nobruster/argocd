from pyflink.table import TableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col, lit
from pyflink.table.window import Tumble

def analyze_restaurant_ratings():
    env_settings = EnvironmentSettings.in_streaming_mode()
    t_env = TableEnvironment.create(environment_settings=env_settings)

    # Set Kafka connector (stable version)
    t_env.get_config().get_configuration().set_string(
        "pipeline.jars",
        "file:///Users/mateusoliveira/Mateus/owshq/GitHub/trn-mst-bdk-2-0/03-apps/flink/jars/flink-sql-connector-kafka-3.2.0-1.19.jar"
    )

    # Define Kafka source table matching your ShadowTraffic schema
    t_env.execute_sql("""
    CREATE TABLE kafka_ratings (
        rating_id BIGINT,
        uuid STRING,
        restaurant_identifier STRING,
        rating DOUBLE,
        `timestamp` TIMESTAMP(3),
        dt_current_timestamp TIMESTAMP(3),
        WATERMARK FOR `timestamp` AS `timestamp` - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'kafka_ratings',
        'properties.bootstrap.servers' = 'localhost:9094',
        'properties.group.id' = 'rating-analyzer-group',
        'value.format' = 'json',
        'scan.startup.mode' = 'earliest-offset'
    )
    """)

    # Alert sink
    t_env.execute_sql("""
    CREATE TABLE print_alert_sink (
        restaurant_identifier STRING,
        previous_avg DOUBLE,
        current_avg DOUBLE,
        window_start TIMESTAMP(3),
        window_end TIMESTAMP(3),
        rating_drop DOUBLE
    ) WITH (
        'connector' = 'print'
    )
    """)

    ratings = t_env.from_path("kafka_ratings")

    # Calculate average rating per restaurant per 24-hour tumbling window
    avg_ratings = ratings \
        .window(Tumble.over(lit(24).hours).on(col("timestamp")).alias("rating_window")) \
        .group_by(col("restaurant_identifier"), col("rating_window")) \
        .select(
            col("restaurant_identifier"),
            col("rating_window").start.alias("window_start"),
            col("rating_window").end.alias("window_end"),
            col("rating").avg.alias("avg_rating")
        )

    t_env.create_temporary_view("avg_ratings", avg_ratings)

    # Detect significant drops compared to previous window (greater than 0.5)
    rating_declines = t_env.sql_query("""
        SELECT
            curr.restaurant_identifier,
            prev.avg_rating AS previous_avg,
            curr.avg_rating AS current_avg,
            curr.window_start,
            curr.window_end,
            (prev.avg_rating - curr.avg_rating) AS rating_drop
        FROM avg_ratings AS curr
        JOIN avg_ratings AS prev
          ON curr.restaurant_identifier = prev.restaurant_identifier
          AND curr.window_start = prev.window_end
        WHERE (prev.avg_rating - curr.avg_rating) > 0.5
    """)

    # Output detected alerts
    rating_declines.execute_insert("print_alert_sink")

    # Keep job running
    print("Rating decline detection is running... Press Ctrl+C to stop.")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Job terminated by user.")


if __name__ == "__main__":
    analyze_restaurant_ratings()
