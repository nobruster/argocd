FROM flink:1.20


# Instala dependências e o Python 3.7
RUN apt-get update -y && \
    apt-get install -y build-essential libssl-dev libbz2-dev liblzma-dev zlib1g-dev lzma libbz2-dev libffi-dev && \
    wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz && \
    tar -xvf Python-3.9.0.tgz && \
    cd Python-3.9.0 && \
    ./configure --without-tests --enable-shared && \
    make -j6 && \
    make install && \
    ldconfig /usr/local/lib && \
    cd .. && rm -f Python-3.9.0.tgz && rm -rf Python-3.9.0 && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Instala o PyFlink
RUN pip3 install apache-flink==1.20.0 apache-beam==2.48.0 pylzma

# Baixa e adicionando plugins
USER root
RUN mkdir -p /opt/flink/plugins/flink-s3-fs-hadoop && \
    wget -O /opt/flink/plugins/flink-s3-fs-hadoop/flink-s3-fs-hadoop.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-s3-fs-hadoop/1.20.0/flink-s3-fs-hadoop-1.20.0.jar

RUN mkdir -p /opt/flink/plugins/paymon-flink && \
    wget -O /opt/flink/plugins/paymon-flink/paymon-flink.jar \
    https://repo.maven.apache.org/maven2/org/apache/paimon/paimon-flink-1.20/1.0.1/paimon-flink-1.20-1.0.1.jar

RUN mkdir -p /opt/flink/plugins/iceberg-flink && \
    wget -O /opt/flink/plugins/iceberg-flink/iceberg-flink-runtime.jar \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-1.20/1.8.0/iceberg-flink-runtime-1.20-1.8.0.jar

# Baixando libs
RUN wget -O /opt/flink/lib/flink-sql-avro-1.20.0.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-avro/1.20.0/flink-sql-avro-1.20.0.jar 

RUN wget -O /opt/flink/lib/flink-connector-kafka-3.3.0-1.20.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.3.0-1.20/flink-connector-kafka-3.3.0-1.20.jar

RUN wget -O /opt/flink/lib/flink-avro-1.20.0.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-avro/1.20.0/flink-avro-1.20.0.jar 

RUN wget -O /opt/flink/lib/flink-sql-avro-confluent-registry-1.20.0.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.20.0/flink-sql-avro-confluent-registry-1.20.0.jar 

RUN wget -O /opt/flink/lib/flink-avro-confluent-registry-1.20.0.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-avro-confluent-registry/1.20.0/flink-avro-confluent-registry-1.20.0.jar

RUN wget -O /opt/flink/lib/avro-1.11.1.jar \
    https://repo1.maven.org/maven2/org/apache/avro/avro/1.11.1/avro-1.11.1.jar

RUN wget -O /opt/flink/lib/commons-beanutils-1.9.4.jar \
    https://repo1.maven.org/maven2/commons-beanutils/commons-beanutils/1.9.4/commons-beanutils-1.9.4.jar

RUN wget -O /opt/flink/lib/flink-connector-kafka-base_2.12-1.11.6.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka-base_2.12/1.11.6/flink-connector-kafka-base_2.12-1.11.6.jar

RUN wget -O /opt/flink/lib/jackson-databind-2.18.3.jar \
    https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.18.3/jackson-databind-2.18.3.jar

RUN wget -O /opt/flink/lib/jackson-core-2.18.3.jar \
    https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.18.3/jackson-core-2.18.3.jar

RUN wget -O /opt/flink/lib/jackson-annotations-2.18.3.jar \
    https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.18.3/jackson-annotations-2.18.3.jar

RUN wget -O /opt/flink/lib/kafka-schema-registry-client-7.9.0.jar \
    https://packages.confluent.io/maven/io/confluent/kafka-schema-registry-client/7.9.0/kafka-schema-registry-client-7.9.0.jar

RUN wget -O /opt/flink/lib/kafka_2.12-3.8.0.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka_2.12/3.8.0/kafka_2.12-3.8.0.jar

RUN wget -O /opt/flink/lib/kafka-clients-3.8.0.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.8.0/kafka-clients-3.8.0.jar

RUN wget -O /opt/flink/lib/connect-api-3.8.0.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/connect-api/3.8.0/connect-api-3.8.0.jar

RUN wget -O /opt/flink/lib/flink-sql-connector-kafka-3.3.0-1.20.jar \
    https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.3.0-1.20/flink-sql-connector-kafka-3.3.0-1.20.jar

    
RUN chown -R flink:flink /opt/flink/lib
RUN chown -R flink:flink /opt/flink/plugins

# Adicionando as aplicacoes python
RUN mkdir /apps
COPY /apps /apps/

# Define o usuário para "flink" novamente
USER flink