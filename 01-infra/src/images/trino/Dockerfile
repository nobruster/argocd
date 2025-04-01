FROM trinodb/trino:465

USER root

# Instalando o jmx
RUN mkdir -p /opt/java_metrics && \
    curl -L -o /opt/java_metrics/jmx_prometheus_javaagent-0.20.0.jar \
    https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.20.0/jmx_prometheus_javaagent-0.20.0.jar

COPY prometheus_config.yaml /opt/java_metrics/config.yaml
RUN chown -R trino:trino /opt/java_metrics

USER trino:trino
