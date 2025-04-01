# Lab 0 - Pipeline de Dados em Streaming de Dados


The lab was developed to demonstrate the capabilities and configurations used to build a data platform inside Kubernetes.



### 0 - Starting the envirionment


```sh
# Initializing the infrastructure - inside the infra/terraform/gitops/argocd folder
terraform init

terraform plan

terraform apply

# If your repository doesn’t work, install it manually
kubectl apply -f ./git-repo-conf.yaml -n gitops

# Keep it in an open terminal
minikube tunnel --profile k8s-minikube
```



### 1 - Running the applications

```sh
# Installing Apache Pinot kubectl apply 
kubectl apply -f ./01-infra/src/app-manifests/datastore/pinot.yaml -n gitops


# Installing Minio Operator and Tenant
kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/deepstore/minio-tenant.yaml -n gitops


# Install Hive Metastore
kubectl apply -f ./01-infra/src/app-manifests/metastore/hive-metastore.yaml -n gitops


# Installing Monitoring
kubectl apply -f ./01-infra/src/app-manifests/monitoring/kube-prometheus.yaml -n gitops


# Installing Flink Operator
kubectl apply -f ./01-infra/src/app-manifests/processing/flink.yaml -n gitops


# Installing Flink Operator
kubectl apply -f ./01-infra/src/app-manifests/processing/flink.yaml -n gitops


# Install Trino
kubectl apply -f ./01-infra/src/app-manifests/processing/trino.yaml -n gitops


# Install Spark Operator
kubectl apply -f ./01-infra/src/app-manifests/processing/spark.yaml -n gitops


# Install Apache Airflow
kubectl apply -f ./01-infra/src/app-manifests/orchestrator/airflow.yaml -n gitops


# Installing Apache Superset
kubectl apply -f ./01-infra/src/app-manifests/visualization/superset.yaml -n gitops


# Installing Strimzi and Kafka
kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-operator.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-broker.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/schema-registry.yaml -n gitops

kubectl apply -f ./01-infra/src/app-manifests/ingestion/strimzi-connect.yaml -n gitops
```



### 2 - Data generation

Initializing data generation via Shadowtraffic.

```sh
kubectl apply -f tests/lab1/shadowtraffic-ubereats-kafka.yaml -n ingestion
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



### 4 - Configuring Apache Pinot

Do a port-forward on the pinot-controller to port 9000

```sh
kubectl port-forward svc/pinot-controller 9000:9000 -n datastore
```

Go to Swagger and use the schemas, then the REALTIME and OFFLINE tables. 




### 4 - Configuring the Flink applications

Create the Flink cluster using the command below:

```sh
kubectl apply -f tests/lab1/flink-cluster-processamento.yaml -n processing

# apply the role if there is a lack of cluster permissions.
kubectl apply -f 01-infra/src/helm-charts/processing/flink-kubernetes-operator/templates/flink-role.yaml -n processing
```


To access the Flink cluster UI, you can run the command below:

```sh
kubectl port-forward svc/flink-cluster-bdk-rest 8081:8081 -n processing
```


Flink jobs can be created via CLI or uploaded to the cluster. To use PyFlink via terminal by connecting to a Flink server, you need to have Flink installed. The commands below are an example of installation:

**These commands will install Flink locally. This may change on other OS, here Linux is used. You can execute these commands inside a pod created specifically for this purpose to avoid problems and conflicts with other libraries**

```sh
# Install Flink on the system
cd /opt 

sudo wget https://dlcdn.apache.org/flink/flink-1.20.1/flink-1.20.1-bin-scala_2.12.tgz

sudo tar -xvzf flink-1.20.1-bin-scala_2.12.tgz

cd flink-1.20.1

# Create a symbolic link to make it easier to use from the terminal
sudo ln -s /opt/flink-1.20.1/bin/* /usr/local/bin/

# Install a compatible version of Java if you don't have it
sudo apt install default-jre

# Set up environment variables - make them persistent in your environment
export FLINK_HOME=/opt/flink-1.20.1
export PATH=$FLINK_HOME/bin:$PATH
export FLINK_CONF_DIR=$FLINK_HOME/conf
export FLINK_LIB_DIR=$FLINK_HOME/lib

# Install Python 3.9 - compatible with PyFlink
sudo apt-get update -y && \
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libffi-dev && \
    wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz && \
    tar -xvf Python-3.9.0.tgz && \
    cd Python-3.9.0 && \
    ./configure --without-tests --enable-shared && \
    make -j6 && \
    sudo make install && \
    sudo ldconfig /usr/local/lib && \
    cd .. && sudo rm -f Python-3.9.0.tgz && sudo rm -rf Python-3.9.0 && \
    sudo ln -s /usr/local/bin/python3 /usr/local/bin/python && \
    sudo apt-get clean

# Install Apache Flink and Apache Beam (required dependency)
pip3.9 install apache-flink==1.20.0 apache-beam==2.48.0

# Test the installation
sudo start-cluster.sh 

sudo flink run /opt/flink-1.20.1/examples/streaming/WordCount.jar --input data.json --output saida-flink

# Check the results and then stop the cluster
sudo stop-cluster.sh

# After installation, run the following commands to execute PyFlink commands on the configured cluster

# Ensure that the topics being used exist and that the required libraries are set up correctly

# Make sure you have access to the cluster and Kafka brokers
pyflink-shell.sh remote localhost 8081
```

Inside the PyFlink shell, execute the commands you want to interact with the Flink cluster.




### 5 - Connect to Superset

Do a port-forward on the pinot-controller to port 8088

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

# Optional configuration for multiquery engine (engine parameters) - https://superset.apache.org/docs/configuration/databases/#apache-pinot
{"connect_args":{"use_multistage_engine":"true"}}
```


After connecting, you need to create a dataset using the new data connection and the necessary tables.

Once that’s done, you can create a dashboard to monitor KPIs.

Tips:

    - You need a data dictionary.

    - Without a data dictionary, you cannot develop a KPI.

    - Shadowtraffic does not have a country code, so you will need a mapping in Pinot or Kafka topics or another source.

    - Flink jobs change the deployment mode depending on the execution mode and cluster criticality.











