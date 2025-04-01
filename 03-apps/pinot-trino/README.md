# Pinot and Trino Lab


This lab was developed to demonstrate the characteristics for streaming data ingestion into Apache Pinot and data exploration using Trino.


### 0 - Inicializando a Plataforma


```sh
# Initializing infrastructure - inside the folder infra/terraform/gitops/argocd
terraform init

terraform plan

terraform apply

# If your repository does not work, install manually
kubectl apply -f ./git-repo-conf.yaml -n gitops

# Keep this terminal open
minikube tunnel --profile k8s-minikube
```



### 1 - Installing Applications

```sh
# Install Trino
kubectl apply -f ./01-infra/src/app-manifests/processing/trino.yaml -n gitops


# Installing Minio Operator and Tenant
kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-tenant.yaml -n gitops


# Install Hive Metastore
kubectl apply -f ./01-infra/src/app-manifests/metastore/hive-metastore.yaml -n gitops


# Installing Apache Pinot
kubectl apply -f ./01-infra/src/app-manifests/datastore/pinot.yaml -n gitops


# Installing Strimzi and Kafka
kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-broker.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/schema-registry.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-connect.yaml -n gitops


# Installing Apache Superset
kubectl apply -f ./01-infra/src/app-manifests/visualization/superset.yaml -n gitops

```



### 2 - Generate Data

Start generating data via Shadowtraffic.

```sh
kubectl apply -f 03-apps/spark-flink/shadowtraffic-ubereats-kafka.yaml -n ingestion
```



### 3 - Configuring Iceberg Table Connectors

Run the sinks to create the Iceberg tables for the topics.

```sh
kubectl delete -f 03-apps/pinot-trino/kafka-connect-sink-iceberg-drivers.yaml -n ingestion

kubectl delete -f 03-apps/pinot-trino/kafka-connect-sink-iceberg-order-status.yaml -n ingestion

kubectl delete -f 03-apps/pinot-trino/kafka-connect-sink-iceberg-ratings.yaml -n ingestion

kubectl delete -f 03-apps/pinot-trino/kafka-connect-sink-iceberg-restaurants.yaml -n ingestion

kubectl delete -f 03-apps/pinot-trino/kafka-connect-sink-iceberg-users.yaml -n ingestion

kubectl delete -f 03-apps/pinot-trino/kafka-connect-sink-iceberg-orders.yaml -n ingestion
```



### 4 - Apache Pinot

Execute the installation script and add the tables and schemas within it.



### 5 - Connect to Superset

Do a port-forward on the pinot-controller on port 8088.

```sh
kubectl port-forward svc/superset 8088:8088 -n visualization
```


Log in to Superset using the username and password:

```sh
admin:admin
```


Create a new database connection for Apache Pinot using the URL below. Check the namespace where Pinot is located.

```sh
# connection URL
pinot://pinot-broker.datastore:8099/query/sql?controller=http://pinot-controller.datastore:9000

# optional configuration for multiquery engine (engine parameters) - https://superset.apache.org/docs/configuration/databases/#apache-pinot
{"connect_args":{"use_multistage_engine":"true"}}
```

### 6 - Running Trino

Run the Trino installation and do the port-forward.

```sh
kubectl port-forward svc/trino 8088:8088 -n trino
```