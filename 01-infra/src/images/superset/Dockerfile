FROM apache/superset

USER root

# Adicionar bibliotecas para se conectar
RUN apt-get update && \
    pip install pinotdb psycopg2-binary sqlalchemy-trino
