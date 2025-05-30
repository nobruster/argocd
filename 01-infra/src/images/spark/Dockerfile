#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

FROM spark:3.4.3

# Switch to user root so we can add additional jars and configuration files.
USER root

# Add the connector jar needed to access S3 FileSystem API.
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.431/aws-java-sdk-bundle-1.12.431.jar $SPARK_HOME/jars/aws-java-sdk-bundle-1.12.431.jar
RUN chmod 644 $SPARK_HOME/jars/aws-java-sdk-bundle-1.12.431.jar
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar $SPARK_HOME/jars/hadoop-common-3.3.4.jar
RUN chmod 644 $SPARK_HOME/jars/hadoop-common-3.3.4.jar
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar $SPARK_HOME/jars/hadoop-aws-3.3.4.jar
RUN chmod 644 $SPARK_HOME/jars/hadoop-aws-3.3.4.jar

# Add iceberg connector jar needed to use Iceberg lakehouse format
ADD https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.4_2.12/1.6.0/iceberg-spark-runtime-3.4_2.12-1.6.0.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/iceberg-spark-runtime-3.4_2.12-1.6.0.jar

# Add Delta connector jar needed to use Delta lakehouse format
ADD https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.3.0/delta-spark_2.12-3.3.0.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/delta-spark_2.12-3.3.0.jar

ADD https://repo1.maven.org/maven2/io/delta/delta-storage/3.3.0/delta-storage-3.3.0.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/delta-storage-3.3.0.jar

# Library to tests and measurement
ADD https://repo1.maven.org/maven2/ch/cern/sparkmeasure/spark-measure_2.12/0.24/spark-measure_2.12-0.24.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/spark-measure_2.12-0.24.jar

ADD https://repo1.maven.org/maven2/com/amazon/deequ/deequ/2.0.8-spark-3.4/deequ-2.0.8-spark-3.4.jar $SPARK_HOME/jars
RUN chmod 644 $SPARK_HOME/jars/deequ-2.0.8-spark-3.4.jar

# Setup for the Prometheus JMX exporter.
ADD https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.11.0/jmx_prometheus_javaagent-0.11.0.jar /prometheus/
RUN chmod 644 /prometheus/jmx_prometheus_javaagent-0.11.0.jar


# Copy the apps to app folders
RUN mkdir -p /app
COPY apps/ /app/
WORKDIR /app

USER ${spark_uid}

RUN mkdir -p /etc/metrics/conf
COPY conf/metrics.properties /etc/metrics/conf
COPY conf/prometheus.yaml /etc/metrics/conf

ENTRYPOINT ["/opt/entrypoint.sh"]
