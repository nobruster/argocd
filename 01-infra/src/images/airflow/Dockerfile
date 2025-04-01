# Imagem de exemplo, altere as bibliotecas e versão de acordo com a necessidade
FROM apache/airflow:2.9.3

# Adicionar programas específicos
# USER root

# RUN apt-get update \
#   && apt-get install -y --no-install-recommends \
#          vim \
#   && apt-get autoremove -yqq --purge \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/* 

USER airflow

# Instalar dependências do Airflow
RUN pip install apache-airflow-providers-cncf-kubernetes

# Configurar o PATH para incluir o diretório caso alguma dependencia precise
# ENV PATH="/home/airflow/.local/bin:${PATH}"

# Limpar o cache do pip para manter a imagem leve
RUN pip cache purge
