# Terraform Scripts to Deployment BDK 2.0

# Comandos para construir os laboratórios

Os laboratórios foram criados de modo que se possa utilizar a máquina local ou uma cloud. Escolha um deles antes de inicializar. O ambiente de cloud pode ter custos associados a sua utilização.

```sh
# Inicializando a infraestrutura - dentro da pasta infra/terraform/platform
# Descomente as variaveis para escolher entre minikube ou eks
# Escolha em qual ambiente de k8s vai utilizar o BDK.
terraform init

terraform plan

terraform apply

# verify if minikube was installed
minikube status --profile k8s-minikube

# caso tenha escolhido o eks
aws eks update-kubeconfig --region us-east-1 --name k8s-aws

```


## Installing ArgoCD

As aplicações são intaladas via manifestos do ArgoCD, para isso, certifique-se que tenha uma instancia do argo funcionando. Este projeto providencia uma instalancia executada via terraform.


```sh
# access argocd folder
# cd infra/terraform/gitops/argocd

terraform init

terraform plan

terraform apply

minikube status --profile k8s-minikube

# ArgoCD Service 
k get svc -n gitops


# enable loadbalancer on minikube {the session must be open in another window}
minikube tunnel --profile k8s-minikube

# create argocd loadbalancer
k patch svc argocd-server -n gitops -p '{"spec": {"type": "LoadBalancer"}}'


# JUST IN CASE
# se o seu repositorio nao funcionar instale manualmente
kubectl apply -f ./git-repo-conf.yaml -n gitops
```

Após a instalação do Argo-CD é necessário executar a aplicação dos manifestos das apps. **Se atente ao detalhe de alterar as configurações de storageclass dependendo do ambiente em que vai rodar os sistemas, por padrão os labs são executados no Minikube.**
