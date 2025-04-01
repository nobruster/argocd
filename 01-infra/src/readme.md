# Deployment of Data Infrastructure Applications using ArgoCD

```sh
# Install Strimzi
kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-operator.yaml -n gitops
kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-broker.yaml -n gitops
kubectl apply -f ./01-infra/src/app-manifests/ingestion/schema-registry.yaml -n gitops
kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-connect.yaml -n gitops


# Install Minio Operator and Tenant
kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-operator.yaml -n gitops
kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-tenant.yaml -n gitops


# Install Spark Operator
kubectl apply -f ./01-infra/src/app-manifests/processing/spark.yaml -n gitops

# Install flink Operator
kubectl apply -f ./01-infra/src/app-manifests/processing/flink.yaml -n gitops


# Install Trino
kubectl apply -f ./01-infra/src/app-manifests/processing/trino.yaml -n gitops


# Install orchestrator
kubectl apply -f ./01-infra/src/app-manifests/orchestrator/airflow.yaml -n gitops
kubectl apply -f ./01-infra/src/app-manifests/orchestrator/kestra.yaml -n gitops


# Install Kestra
kubectl apply -f ./01-infra/src/app-manifests/orchestrator/kestra.yaml -n gitops


# Install Apache Superset
kubectl apply -f ./01-infra/src/app-manifests/visualization/superset.yaml -n gitops


# Install Hive Metastore
kubectl apply -f ./01-infra/src/app-manifests/metastore/hive-metastore.yaml -n gitops


# Install Apache Pinot
kubectl apply -f ./01-infra/src/app-manifests/datastore/pinot.yaml -n gitops


# Install MLFlow
kubectl apply -f ./01-infra/src/app-manifests/learning/mlflow.yaml -n gitops


# Install Monitoring
kubectl apply -f ./01-infra/src/app-manifests/monitoring/kube-prometheus.yaml -n gitops
```


## Tips 

* Modify the types of disks used. For Minikube, use standard or leave it blank; for EKS, use gp2 or others.
* Applies to: Pinot, Pinot Zookeeper, Minio Tenant, Airflow Postgres, Superset Postgres, Hive Postgres, Strimzi Broker, Kestra.
* More than one chart file may need to be accessed to change disk types.
* Use spot instances from cloud providers to reduce costs for testing and study purposes.
* Whenever deleting a cloud cluster, check the provider’s dashboard to ensure no resources are left behind to avoid unnecessary charges.


## Manual Installation using Helm Command Lines

#### Configuring the Charts Used

The installation is managed via ArgoCD, and the base files are the official Helm charts of the applications. However, not all applications have official Helm charts, so they were installed using manifests created based on their documentation.


```sh
# Configure Repos
helm repo add minio-operator https://operator.min.io
helm repo add spark-operator https://kubeflow.github.io/spark-operator
helm repo add heva-helm-charts https://hevaweb.github.io/heva-helm-charts/
helm repo add trino https://trinodb.github.io/charts
helm repo add strimzi https://strimzi.io/charts/
helm repo add flink https://downloads.apache.org/flink/flink-kubernetes-operator-1.10.0/
helm repo add argo https://argoproj.github.io/argo-helm
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/helm
helm repo add superset https://apache.github.io/superset
helm repo add apache-airflow https://airflow.apache.org
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add kestra https://helm.kestra.io/
helm repo add mlflow https://community-charts.github.io/helm-charts

# update repos
helm repo update
```

## Download charts

```sh
# Download charts to src folder
helm pull minio-operator/operator --version 7.0.0 --untar --untardir ./src/helm-charts/deepstore
helm pull minio-operator/tenant --version 7.0.0 --untar --untardir ./src/helm-charts/deepstore
helm pull spark-operator/spark-operator --version 2.1.0 --untar --untardir ./src/helm-charts/processing
helm pull heva-helm-charts/hive-metastore --version 0.0.1 --untar --untardir ./src/helm-charts/deepstore
helm pull trino/trino --version 1.37.0 --untar --untardir ./src/helm-charts/processing
helm pull strimzi/strimzi-kafka-operator --version 0.45.0 --untar --untardir ./src/helm-charts/ingestion
helm pull flink/flink-kubernetes-operator --version 1.10.0 --untar --untardir ./src/helm-charts/processing
helm pull argo/argo-cd --version 7.8.2 --untar --untardir ./src/helm-charts/gitops
helm pull pinot/pinot --version 0.3.0 --untar --untardir ./src/helm-charts/datastore
helm pull superset/superset --version 0.14.0 --untar --untardir ./src/helm-charts/visualization
helm pull apache-airflow/airflow --version 1.15.0 --untar --untardir ./src/helm-charts/orchestrator
helm pull prometheus-community/kube-prometheus-stack --version 69.3.2 --untar --untardir ./src/helm-charts/monitoring
helm pull bitnami/postgresql --version 12.0.0 --untar --untardir ./src/helm-charts/deepstore
helm pull kestra/kestra --version 0.21.4 --untar --untardir ./src/helm-charts/orchestrator
helm pull mlflow/mlflow --version 0.13.1 --untar --untardir ./src/helm-charts/learning
```


## Creating namespaces

```sh
# create the namespace manually
kubectl create namespace datastore
kubectl create namespace deepstore
kubectl create namespace ingestion
kubectl create namespace monitoring
kubectl create namespace orchestrator
kubectl create namespace processing
kubectl create namespace visualization
kubectl create namespace learning
```

After that install the selected applications using helm insall.

```sh
# example of one install
helm install srtimzi-operator ./01-infra/src/helm-charts/ingestion/strimzi-kafka-operator -f ./01-infra/src/helm-charts/ingestion/strimzi-kafka-operator/values.yaml -n ingestion
```

