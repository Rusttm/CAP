Docker installation
from https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
1. curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
2. cd /airdocker
3. mkdir ./dags ./logs ./plugins
4. echo -e "AIRFLOW_UID=$(id -u)" > .env
5. $ docker-compose up airflow-init
6. $ docker compose up

Docker dependencies installation
1. make requirements.txt
2. make Dockerfile
   2.1 if you want to use venv, you need use the dockerkit (see https://docs.docker.com/build/buildkit/)
   2.2 DOCKER_BUILDKIT=1 docker build .
   2.3 To use Docker BuildKit by default, edit the Docker daemon configuration in /etc/docker/daemon.json as follows, and restart the daemon ({"features": {"buildkit": true } }).
3. $ docker build . --tag extended_airflow:latest
4. make changes in yaml: 
   image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.2} to image: ${AIRFLOW_IMAGE_NAME:-extended_airflow:latest}
5. write test dag
6. $ docker compose up airflow-init
# this code not works cause no postgres base
# 6. $ docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler 
# 7. if changes permissions sudo chmod -R 777