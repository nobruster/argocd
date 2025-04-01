# kafka version = 3.7.1
# get image from strimzi repository
# https://quay.io/repository/strimzi/kafka
FROM quay.io/strimzi/kafka:latest-kafka-3.8.0


# using root user
USER root:root


# Criando os diretorios dos conectores
RUN mkdir -p /opt/kafka/plugins/confluentinc-kafka-connect-jdbc
RUN mkdir -p /opt/kafka/plugins/confluentinc-kafka-connect-s3
RUN mkdir -p /opt/kafka/plugins/kafka-connect-aws-s3
RUN mkdir -p /opt/kafka/plugins/kafka-connect-ftp
RUN mkdir -p /opt/kafka/plugins/kafka-connect-http
RUN mkdir -p /opt/kafka/plugins/iceberg-kafka-connect-runtime-hive


# Links para baixar os conectaores localmente
# https://hub-downloads.confluent.io/api/plugins/confluentinc/kafka-connect-jdbc/versions/10.8.1/confluentinc-kafka-connect-jdbc-10.8.1.zip
# https://hub-downloads.confluent.io/api/plugins/confluentinc/kafka-connect-s3/versions/10.5.23/confluentinc-kafka-connect-s3-10.5.23.zip
# https://github.com/lensesio/stream-reactor/releases/download/8.1.28/kafka-connect-aws-s3-8.1.28.zip
# https://github.com/lensesio/stream-reactor/releases/download/8.1.28/kafka-connect-ftp-8.1.28.zip
# https://github.com/databricks/iceberg-kafka-connect/releases/download/v0.6.19/iceberg-kafka-connect-runtime-hive-0.6.19.zip

# Copie os conectores para dentro da imagem do kafka. Copiar somentes os jars
COPY connectors/confluentinc-kafka-connect-jdbc-10.8.0/ /opt/kafka/plugins/confluentinc-kafka-connect-jdbc/
COPY connectors/confluentinc-kafka-connect-s3-10.5.19/ /opt/kafka/plugins/confluentinc-kafka-connect-s3/
COPY connectors/kafka-connect-aws-s3-8.1.22/ /opt/kafka/plugins/kafka-connect-aws-s3/
COPY connectors/kafka-connect-ftp-8.1.22/ /opt/kafka/plugins/kafka-connect-ftp/
COPY connectors/iceberg-kafka-connect-runtime-hive-0.6.19/ /opt/kafka/plugins/iceberg-kafka-connect-runtime-hive/


# Links para baixar bibliotecas usadas
# https://repo1.maven.org/maven2/org/apache/avro/avro/1.11.0/avro-1.11.0.jar
# https://packages.confluent.io/maven/io/confluent/common-config/7.7.0/common-config-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/common-utils/7.7.0/common-utils-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-avro-serializer/7.7.0/kafka-avro-serializer-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-connect-avro-converter/7.7.0/kafka-connect-avro-converter-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-connect-avro-data/7.7.0/kafka-connect-avro-data-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-connect-json-schema-converter/7.7.0/kafka-connect-json-schema-converter-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-json-schema-provider/7.7.0/kafka-json-schema-provider-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-json-schema-serializer/7.7.0/kafka-json-schema-serializer-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-schema-registry-client/7.7.0/kafka-schema-registry-client-7.7.0.jar
# https://packages.confluent.io/maven/io/confluent/kafka-schema-serializer/7.7.0/kafka-schema-serializer-7.7.0.jar
# https://hub-downloads.confluent.io/api/plugins/confluentinc/kafka-connect-avro-converter/versions/7.9.0/confluentinc-kafka-connect-avro-converter-7.9.0.zip


# Copiando as bibliotecas para a pasta lib
COPY libs/ /opt/kafka/libs/
COPY connectors/confluentinc-kafka-connect-avro-converter-7.7.0/ /opt/kafka/libs/


# user
USER 1001