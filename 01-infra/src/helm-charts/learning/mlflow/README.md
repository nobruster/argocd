# mlflow

![mlflow](https://raw.githubusercontent.com/mlflow/mlflow/master/docs/source/_static/MLflow-logo-final-black.png)

A Helm chart for Mlflow open source platform for the machine learning lifecycle

![Version: 0.13.1](https://img.shields.io/badge/Version-0.13.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 2.20.2](https://img.shields.io/badge/AppVersion-2.20.2-informational?style=flat-square)

## Get Helm Repository Info

```console
helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo update
```

_See [`helm repo`](https://helm.sh/docs/helm/helm_repo/) for command documentation._

## Installing the Chart

```console
helm install [RELEASE_NAME] community-charts/mlflow
```

_See [configuration](#configuration) below._

_See [helm install](https://helm.sh/docs/helm/helm_install/) for command documentation._

> **Tip**: Search all available chart versions using `helm search repo community-charts -l`. Please don't forget to run `helm repo update` before the command.

## Supported Databases

Currently, we support the following two databases as a backend repository for Mlflow.

* [PostgreSQL](https://www.postgresql.org/)
* [MySQL](https://www.mysql.com/)

## Supported Cloud Providers

We currently support the following three cloud providers for [BLOB](https://de.wikipedia.org/wiki/Binary_Large_Object) storage integration.

* [AWS (S3)](https://aws.amazon.com/s3/)
* [Google Cloud Platform (Cloud Storage)](https://cloud.google.com/storage)
* [Azure Cloud (Azure Blob Storage)](https://azure.microsoft.com/en-us/services/storage/blobs/)

## Values Files Examples

## Postgres Database Migration Values Files Example

```yaml
backendStore:
  databaseMigration: true
  postgres:
    enabled: true
    host: "postgresql-instance1.cg034hpkmmjt.eu-central-1.rds.amazonaws.com"
    port: 5432
    database: "mlflow"
    user: "mlflowuser"
    password: "Pa33w0rd!"
```

## MySQL Database Migration Values Files Example

```yaml
backendStore:
  databaseMigration: true
  mysql:
    enabled: true
    host: "mysql-instance1.cg034hpkmmjt.eu-central-1.rds.amazonaws.com"
    port: 3306
    database: "mlflow"
    user: "mlflowuser"
    password: "Pa33w0rd!"
```

## Postgres Database Connection Check Values Files Example

```yaml
backendStore:
  databaseConnectionCheck: true
  postgres:
    enabled: true
    host: "postgresql-instance1.cg034hpkmmjt.eu-central-1.rds.amazonaws.com"
    port: 5432
    database: "mlflow"
    user: "mlflowuser"
    password: "Pa33w0rd!"
```

## MySQL Database Connection Check Values Files Example

```yaml
backendStore:
  databaseConnectionCheck: true
  mysql:
    enabled: true
    host: "mysql-instance1.cg034hpkmmjt.eu-central-1.rds.amazonaws.com"
    port: 3306
    database: "mlflow"
    user: "mlflowuser"
    password: "Pa33w0rd!"
```

## AWS Installation Examples

You can use 2 different way to connect your S3 backend.

- First way, you can access to your S3 with IAM user's awsAccessKeyId and awsSecretAccessKey.
- Second way, you can create an aws role for your service account. And you can assign your role ARN from serviceAccount annotation. You don't need to create or manage IAM user anymore. Please find more information from [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html).

> **Tip**: Please follow [this tutorial](https://aws.amazon.com/getting-started/hands-on/create-connect-postgresql-db/) to create your own RDS postgres cluster.

## S3 (Minio) and PostgreSQL DB Configuration on Helm Upgrade Command Example

```console
helm upgrade --install mlflow community-charts/mlflow \
  --set backendStore.databaseMigration=true \
  --set backendStore.postgres.enabled=true \
  --set backendStore.postgres.host=postgres-service \
  --set backendStore.postgres.port=5432 \
  --set backendStore.postgres.database=postgres \
  --set backendStore.postgres.user=postgres \
  --set backendStore.postgres.password=postgres \
  --set artifactRoot.s3.enabled=true \
  --set artifactRoot.s3.bucket=mlflow \
  --set artifactRoot.s3.awsAccessKeyId=minioadmin \
  --set artifactRoot.s3.awsSecretAccessKey=minioadmin \
  --set extraEnvVars.MLFLOW_S3_ENDPOINT_URL=http://minio-service:9000 \
  --set serviceMonitor.enabled=true
```

## S3 (Minio) and MySQL DB Configuration on Helm Upgrade Command Example

```console
helm upgrade --install mlflow community-charts/mlflow \
  --set backendStore.databaseMigration=true \
  --set backendStore.mysql.enabled=true \
  --set backendStore.mysql.host=mysql-service \
  --set backendStore.mysql.port=3306 \
  --set backendStore.mysql.database=mlflow \
  --set backendStore.mysql.user=mlflow \
  --set backendStore.mysql.password=mlflow \
  --set artifactRoot.s3.enabled=true \
  --set artifactRoot.s3.bucket=mlflow \
  --set artifactRoot.s3.awsAccessKeyId=minioadmin \
  --set artifactRoot.s3.awsSecretAccessKey=minioadmin \
  --set extraEnvVars.MLFLOW_S3_ENDPOINT_URL=http://minio-service:9000 \
  --set serviceMonitor.enabled=true
```

## S3 Access with awsAccessKeyId and awsSecretAccessKey Values Files Example

```yaml
backendStore:
  postgres:
    enabled: true
    host: "postgresql-instance1.cg034hpkmmjt.eu-central-1.rds.amazonaws.com"
    port: 5432
    database: "mlflow"
    user: "mlflowuser"
    password: "Pa33w0rd!"

artifactRoot:
  s3:
    enabled: true
    bucket: "my-mlflow-artifact-root-backend"
    awsAccessKeyId: "a1b2c3d4"
    awsSecretAccessKey: "a1b2c3d4"
```

## S3 Access with AWS EKS Role ARN Values Files Example

> **Tip**: [Associate an IAM role to a service account](https://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html)

```yaml
serviceAccount:
  create: true
  annotations:
    eks.amazonaws.com/role-arn: "arn:aws:iam::account-id:role/iam-role-name"
  name: "mlflow"

backendStore:
  postgres:
    enabled: true
    host: "postgresql-instance1.cg034hpkmmjt.eu-central-1.rds.amazonaws.com"
    port: 5432
    database: "mlflow"
    user: "mlflowuser"
    password: "Pa33w0rd!"

artifactRoot:
  s3:
    enabled: true
    bucket: "my-mlflow-artifact-root-backend"
```

## Azure Cloud Installation Example

> **Tip**: Please follow [this tutorial](https://docs.microsoft.com/en-us/azure/postgresql/tutorial-design-database-using-azure-portal) to create your own postgres database.
> **Tip**: Please follow [this tutorial](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) to create your azure blob storage and container.

```yaml
backendStore:
  postgres:
    enabled: true
    host: "mydemoserver.postgres.database.azure.com"
    port: 5432
    database: "mlflow"
    user: "mlflowuser"
    password: "Pa33w0rd!"

artifactRoot:
  azureBlob:
    enabled: true
    container: "mlflow"
    storageAccount: "mystorageaccount"
    accessKey: "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="
```

## Authentication Example

> **Tip**: auth and ldapAuth can not be enabled at same time!

```yaml
auth:
  enabled: true
  adminUsername: "admin"
  adminPassword: "S3cr3+"
```

Use following configuration for centralised PosgreSQL DB backend for authentication backend.

```yaml
auth:
  enabled: true
  adminUsername: "admin"
  adminPassword: "S3cr3+"
  postgres:
    enabled: true
    host: "postgresql--auth-instance1.abcdef1234.eu-central-1.rds.amazonaws.com"
    port: 5432
    database: "auth"
    user: "mlflowauth"
    password: "A4m1nPa33w0rd!"
```

## Basic Authentication with LDAP Backend

> **Tip**: auth and ldapAuth can not be enabled at same time!

```yaml
ldapAuth:
  enabled: true
  uri: "ldap://lldap:3890/dc=mlflow,dc=test"
  lookupBind: "uid=%s,ou=people,dc=mlflow,dc=test"
  groupAttribute: "dn"
  searchBaseDistinguishedName: "ou=groups,dc=mlflow,dc=test"
  searchFilter: "(&(objectclass=groupOfUniqueNames)(uniquemember=%s))"
  adminGroupDistinguishedName: "cn=test-admin,ou=groups,dc=mlflow,dc=test"
  userGroupDistinguishedName: "cn=test-user,ou=groups,dc=mlflow,dc=test"
```

## Requirements

Kubernetes: `>=1.16.0-0`

## Uninstall Helm Chart

```console
helm uninstall [RELEASE_NAME]
```

This removes all the Kubernetes components associated with the chart and deletes the release.

_See [helm uninstall](https://helm.sh/docs/helm/helm_uninstall/) for command documentation._

## Upgrading Chart

```console
helm upgrade [RELEASE_NAME] community-charts/mlflow
```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | For more information checkout: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity |
| artifactRoot.azureBlob.accessKey | string | `""` | Azure Cloud Storage Account Access Key for the container |
| artifactRoot.azureBlob.connectionString | string | `""` | Azure Cloud Connection String for the container. Only onnectionString or accessKey required |
| artifactRoot.azureBlob.container | string | `""` | Azure blob container name |
| artifactRoot.azureBlob.enabled | bool | `false` | Specifies if you want to use Azure Blob Storage Mlflow Artifact Root |
| artifactRoot.azureBlob.path | string | `""` | Azure blobk container folder. If you want to use root level, please don't set anything. |
| artifactRoot.azureBlob.storageAccount | string | `""` | Azure storage account name |
| artifactRoot.gcs.bucket | string | `""` | Google Cloud Storage bucket name |
| artifactRoot.gcs.enabled | bool | `false` | Specifies if you want to use Google Cloud Storage Mlflow Artifact Root |
| artifactRoot.gcs.path | string | `""` | Google Cloud Storage bucket folder. If you want to use root level, please don't set anything. |
| artifactRoot.proxiedArtifactStorage | bool | `false` | Specifies if you want to enable proxied artifact storage access |
| artifactRoot.s3.awsAccessKeyId | string | `""` | AWS IAM user AWS_ACCESS_KEY_ID which has attached policy for access to the S3 bucket |
| artifactRoot.s3.awsSecretAccessKey | string | `""` | AWS IAM user AWS_SECRET_ACCESS_KEY which has attached policy for access to the S3 bucket |
| artifactRoot.s3.bucket | string | `""` | S3 bucket name |
| artifactRoot.s3.enabled | bool | `false` | Specifies if you want to use AWS S3 Mlflow Artifact Root |
| artifactRoot.s3.path | string | `""` | S3 bucket folder. If you want to use root level, please don't set anything. |
| auth | object | `{"adminPassword":"","adminUsername":"","appName":"basic-auth","authorizationFunction":"mlflow.server.auth:authenticate_request_basic_auth","configFile":"basic_auth.ini","configPath":"/etc/mlflow/auth/","defaultPermission":"READ","enabled":false,"postgres":{"database":"","driver":"","enabled":false,"host":"","password":"","port":5432,"user":""},"sqliteFile":"basic_auth.db","sqliteFullPath":""}` | Mlflow authentication settings |
| auth.adminPassword | string | `""` | Mlflow admin user password |
| auth.adminUsername | string | `""` | Mlflow admin user username |
| auth.appName | string | `"basic-auth"` | Default registered authentication app name. If you want to use your custom authentication function, please look at: https://mlflow.org/docs/latest/auth/index.html#custom-authentication |
| auth.authorizationFunction | string | `"mlflow.server.auth:authenticate_request_basic_auth"` | Default authentication function |
| auth.configFile | string | `"basic_auth.ini"` | Mlflow authentication INI file |
| auth.configPath | string | `"/etc/mlflow/auth/"` | Mlflow authentication INI configuration file path. |
| auth.defaultPermission | string | `"READ"` | Default permission for all users. More details: https://mlflow.org/docs/latest/auth/index.html#permissions |
| auth.enabled | bool | `false` | Specifies if you want to enable mlflow authentication. auth and ldapAuth can't be enabled at same time. |
| auth.postgres | object | `{"database":"","driver":"","enabled":false,"host":"","password":"","port":5432,"user":""}` | PostgreSQL based centrilised authentication database |
| auth.postgres.database | string | `""` | mlflow authorization database name created before in the postgres instance |
| auth.postgres.driver | string | `""` | postgres database connection driver. e.g.: "psycopg2" |
| auth.postgres.enabled | bool | `false` | Specifies if you want to use postgres auth backend storage |
| auth.postgres.host | string | `""` | Postgres host address. e.g. your RDS or Azure Postgres Service endpoint |
| auth.postgres.password | string | `""` | postgres database user password which can access to mlflow authorization database |
| auth.postgres.port | int | `5432` | Postgres service port |
| auth.postgres.user | string | `""` | postgres database user name which can access to mlflow authorization database |
| auth.sqliteFile | string | `"basic_auth.db"` | SQLite database file |
| auth.sqliteFullPath | string | `""` | SQLite database folder. Default is user home directory. |
| backendStore | object | `{"databaseConnectionCheck":false,"databaseMigration":false,"mysql":{"database":"","driver":"pymysql","enabled":false,"host":"","password":"","port":3306,"user":""},"postgres":{"database":"","driver":"","enabled":false,"host":"","password":"","port":5432,"user":""}}` | Mlflow database connection settings |
| backendStore.databaseConnectionCheck | bool | `false` | Add an additional init container, which checks for database availability |
| backendStore.databaseMigration | bool | `false` | Specifies if you want to run database migration |
| backendStore.mysql.database | string | `""` | mlflow database name created before in the mysql instance |
| backendStore.mysql.driver | string | `"pymysql"` | mysql database connection driver. e.g.: "pymysql" |
| backendStore.mysql.enabled | bool | `false` | Specifies if you want to use mysql backend storage |
| backendStore.mysql.host | string | `""` | MySQL host address. e.g. your Amazon RDS for MySQL |
| backendStore.mysql.password | string | `""` | mysql database user password which can access to mlflow database |
| backendStore.mysql.port | int | `3306` | MySQL service port |
| backendStore.mysql.user | string | `""` | mysql database user name which can access to mlflow database |
| backendStore.postgres.database | string | `""` | mlflow database name created before in the postgres instance |
| backendStore.postgres.driver | string | `""` | postgres database connection driver. e.g.: "psycopg2" |
| backendStore.postgres.enabled | bool | `false` | Specifies if you want to use postgres backend storage |
| backendStore.postgres.host | string | `""` | Postgres host address. e.g. your RDS or Azure Postgres Service endpoint |
| backendStore.postgres.password | string | `""` | postgres database user password which can access to mlflow database |
| backendStore.postgres.port | int | `5432` | Postgres service port |
| backendStore.postgres.user | string | `""` | postgres database user name which can access to mlflow database |
| extraArgs | object | `{}` | A map of arguments and values to pass to the `mlflow server` command. Keys must be camelcase. Helm will turn them to kebabcase style. |
| extraContainers | list | `[]` | Extra containers for the mlflow pod |
| extraEnvVars | object | `{}` | Extra environment variables |
| extraFlags | list | `[]` | A list of flags to pass to `mlflow server` command. Items must be camelcase. Helm will turn them to kebabcase style. |
| extraSecretNamesForEnvFrom | list | `[]` | Extra secrets for environment variables |
| extraVolumeMounts | list | `[]` | Extra Volume Mounts for the mlflow container |
| extraVolumes | list | `[]` | Extra Volumes for the pod |
| flaskServerSecretKey | string | `""` | Mlflow Flask Server Secret Key. Default: Will be auto generated. |
| fullnameOverride | string | `""` | String to override the default generated fullname |
| image.pullPolicy | string | `"IfNotPresent"` | The docker image pull policy |
| image.repository | string | `"burakince/mlflow"` | The docker image repository to use |
| image.tag | string | `""` | The docker image tag to use. Default app version |
| imagePullSecrets | list | `[]` | Image pull secrets for private docker registry usages |
| ingress.annotations | object | `{}` | Additional ingress annotations |
| ingress.className | string | `""` | New style ingress class name. Only possible if you use K8s 1.18.0 or later version |
| ingress.enabled | bool | `false` | Specifies if you want to create an ingress access |
| ingress.hosts[0].host | string | `"chart-example.local"` |  |
| ingress.hosts[0].paths[0].path | string | `"/"` |  |
| ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` | Ingress path type |
| ingress.tls | list | `[]` | Ingress tls configuration for https access |
| initContainers | list | `[]` | Init Containers for Mlflow Pod |
| ldapAuth | object | `{"adminGroupDistinguishedName":"","enabled":false,"groupAttribute":"dn","lookupBind":"","searchBaseDistinguishedName":"","searchFilter":"(&(objectclass=groupOfUniqueNames)(uniquemember=%s))","uri":"","userGroupDistinguishedName":""}` | Basic Authentication with LDAP backend |
| ldapAuth.adminGroupDistinguishedName | string | `""` | LDAP DN for the admin group. e.g.: "cn=test-admin,ou=groups,dc=mlflow,dc=test" |
| ldapAuth.enabled | bool | `false` | Specifies if you want to enable mlflow LDAP authentication. auth and ldapAuth can't be enabled at same time. |
| ldapAuth.groupAttribute | string | `"dn"` | LDAP group attribute. |
| ldapAuth.lookupBind | string | `""` | LDAP Loopup Bind. e.g.: "uid=%s,ou=people,dc=mlflow,dc=test" |
| ldapAuth.searchBaseDistinguishedName | string | `""` | LDAP base DN for the search. e.g.: "ou=groups,dc=mlflow,dc=test" |
| ldapAuth.searchFilter | string | `"(&(objectclass=groupOfUniqueNames)(uniquemember=%s))"` | LDAP query filter for search |
| ldapAuth.uri | string | `""` | LDAP URI. e.g.: "ldap://lldap:3890/dc=mlflow,dc=test" |
| ldapAuth.userGroupDistinguishedName | string | `""` | LDAP DN for the user group. e.g.: "cn=test-user,ou=groups,dc=mlflow,dc=test" |
| livenessProbe | object | `{"failureThreshold":5,"initialDelaySeconds":10,"periodSeconds":30,"timeoutSeconds":3}` | Liveness probe configurations. Please look to [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes). |
| nameOverride | string | `""` | String to override the default generated name |
| nodeSelector | object | `{}` | For more information checkout: https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector |
| podAnnotations | object | `{}` | Annotations for the pod |
| podSecurityContext | object | `{}` | This is for setting Security Context to a Pod. For more information checkout: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ |
| readinessProbe | object | `{"failureThreshold":5,"initialDelaySeconds":10,"periodSeconds":30,"timeoutSeconds":3}` | Readiness probe configurations. Please look to [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes). |
| replicaCount | int | `1` | Numbers of replicas |
| resources | object | `{}` | This block is for setting up the resource management for the pod more information can be found here: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/ |
| securityContext | object | `{}` | This is for setting Security Context to a Container. For more information checkout: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ |
| service | object | `{"annotations":{},"name":"http","port":5000,"type":"ClusterIP"}` | This is for setting up a service more information can be found here: https://kubernetes.io/docs/concepts/services-networking/service/ |
| service.annotations | object | `{}` | Additional service annotations |
| service.name | string | `"http"` | Default Service name |
| service.port | int | `5000` | This sets the ports more information can be found here: https://kubernetes.io/docs/concepts/services-networking/service/#field-spec-ports |
| service.type | string | `"ClusterIP"` | This sets the service type more information can be found here: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account. AWS EKS users can assign role arn from here. Please find more information from here: https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html |
| serviceAccount.automount | bool | `true` | Automatically mount a ServiceAccount's API credentials? |
| serviceAccount.create | bool | `true` | Specifies whether a ServiceAccount should be created |
| serviceAccount.name | string | `""` | The name of the ServiceAccount to use. If not set and create is true, a name is generated using the fullname template |
| serviceMonitor.enabled | bool | `false` | When set true then use a ServiceMonitor to configure scraping |
| serviceMonitor.interval | string | `"30s"` | Set how frequently Prometheus should scrape |
| serviceMonitor.labels | object | `{"release":"prometheus"}` | Set labels for the ServiceMonitor, use this to define your scrape label for Prometheus Operator |
| serviceMonitor.labels.release | string | `"prometheus"` | default `kube prometheus stack` helm chart serviceMonitor selector label Mostly it's your prometheus helm release name. Please find more information from here: https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/troubleshooting.md#troubleshooting-servicemonitor-changes |
| serviceMonitor.metricRelabelings | list | `[]` | Set of rules to relabel your exist metric labels |
| serviceMonitor.namespace | string | `"monitoring"` | Set the namespace the ServiceMonitor should be deployed |
| serviceMonitor.targetLabels | list | `[]` | Set of labels to transfer on the Kubernetes Service onto the target. |
| serviceMonitor.telemetryPath | string | `"/metrics"` | Set path to mlflow telemtery-path |
| serviceMonitor.timeout | string | `"10s"` | Set timeout for scrape |
| serviceMonitor.useServicePort | bool | `false` | When set true then use a service port. On default use a pod port. |
| strategy | object | `{"rollingUpdate":{"maxSurge":"100%","maxUnavailable":0},"type":"RollingUpdate"}` | This will set the deployment strategy more information can be found here: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy |
| tolerations | list | `[]` | For more information checkout: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ |

**Homepage:** <https://mlflow.org>

## Source Code

* <https://github.com/community-charts/helm-charts>
* <https://github.com/burakince/mlflow>
* <https://github.com/mlflow/mlflow>

## Chart Development

Please install unittest helm plugin with `helm plugin install https://github.com/helm-unittest/helm-unittest.git` command and use following command to run helm unit tests.

```console
helm unittest --strict --file 'unittests/**/*.yaml' charts/mlflow
```

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| burakince | <burak.ince@linux.org.tr> | <https://www.burakince.com> |
