# Spark and Flink


This lab was developed to demonstrate how to use Spark and Flink in a data architecture.


### 0 - Initializing the Platform


```sh
# Initializing the infrastructure - inside the folder infra/terraform/gitops/argocd
terraform init

terraform plan

terraform apply

# If your repository does not work, install manually
kubectl apply -f ./git-repo-conf.yaml -n gitops

# Keep this terminal open
minikube tunnel --profile k8s-minikube
```



### 1 - Instalar as aplicacoes

```sh
# Installing Minio Operator and Tenant
kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-tenant.yaml -n gitops


# Install Hive Metastore
kubectl apply -f ./01-infra/src/app-manifests/metastore/hive-metastore.yaml -n gitops


# Install Spark Operator
kubectl apply -f ./01-infra/src/app-manifests/processing/spark.yaml -n gitops


# Installing Flink Operator
kubectl apply -f ./01-infra/src/app-manifests/processing/flink.yaml -n gitops


# Installing Strimzi and Kafka
kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-broker.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/schema-registry.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-connect.yaml -n gitops
```



### 2 - Generating Data

Start generating data via Shadowtraffic.

```sh
kubectl apply -f 03-apps/spark-flink/shadowtraffic-ubereats-kafka.yaml -n ingestion
```



### 3 - Configuring Iceberg Table Connectors

Run the sinks to create Iceberg tables for the topics.

```sh
kubectl apply -f 03-apps/spark-flink/kafka-connect-sink-iceberg-drivers.yaml -n ingestion

kubectl apply -f 03-apps/spark-flink/kafka-connect-sink-iceberg-order-status.yaml -n ingestion

kubectl apply -f 03-apps/spark-flink/kafka-connect-sink-iceberg-ratings.yaml -n ingestion

kubectl apply -f 03-apps/spark-flink/kafka-connect-sink-iceberg-restaurants.yaml -n ingestion

kubectl apply -f 03-apps/spark-flink/kafka-connect-sink-iceberg-users.yaml -n ingestion

kubectl apply -f 03-apps/spark-flink/kafka-connect-sink-iceberg-orders.yaml -n ingestion
```



### 4 - Apache Flink

```sh
# Running Flink cluster
kubectl delete -f 03-apps/spark-flink/flink-cluster.yaml -n processing

pyflink-shell.sh remote localhost 8081
```



### 5 - Apache Spark

Run the installation script and check if the buckets and tables exist. Verify if the PySpark files are in the buckets. After that, you can run the spark-operator YAML.
