# Kafka and Minio


This lab was developed to demonstrate the characteristics and technologies used for streaming data ingestion.




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



### 1 - Installing the Applications

```sh
# Installing Minio Operator and Tenant
kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-tenant.yaml -n gitops


# Installing Monitoring
kubectl apply -f ./01-infra/src/app-manifests/monitoring/kube-prometheus.yaml -n gitops


# Install Hive Metastore
kubectl apply -f ./01-infra/src/app-manifests/metastore/hive-metastore.yaml -n gitops



# Installing Strimzi and Kafka
kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-broker.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/schema-registry.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-connect.yaml -n gitops
```



### 2 - Generating Data

Start generating data via Shadowtraffic.

```sh
kubectl apply -f tests/lab2/shadowtraffic-ubereats-kafka.yaml -n ingestion
```



### 3 - Configuring Iceberg Table Connectors

Run the sinks to create the Iceberg tables for the topics.

```sh
kubectl apply -f tests/lab2/kafka-connect-sink-iceberg-drivers.yaml -n ingestion

kubectl apply -f tests/lab2/kafka-connect-sink-iceberg-order-status.yaml -n ingestion
```

