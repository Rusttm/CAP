New test module for scheduling updates


* Instalation with in venv 
* working directory /Users/johnlennon/RusttmGDrive/Python/CAP/Airflow/airhome* 
* venv air_env
from https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html:
1. $ pip freeze | xargs pip uninstall -y
2. $ pip install "apache-airflow==2.6.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.2/constraints-3.7.txt"
3. $ export AIRFLOW_HOME=/Users/johnlennon/RusttmGDrive/Python/CAP/Airflow/airhome
4. $ airflow db init 
5. $ airflow webserver -p 8081
6. $ airflow users create  --username root --firstname firstname --lastname lastname --role Admin --email admin@domain.com
in new terminal
7. $ export AIRFLOW_HOME=/Users/johnlennon/RusttmGDrive/Python/CAP/Airflow/airhome
8. $ airflow scheduler

# $ pip install airflow['all']
# $ pip install -r requirements.txt

Docker installation
from https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
1. curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.6.2/docker-compose.yaml'
2. cd /airhome
3. mkdir ./dags ./logs ./plugins
4. echo -e "AIRFLOW_UID=$(id -u)" > .env
5. $ docker-compose up airflow-init
6. $ docker compose up

Docker dependencies installation
1. make requirements.txt
2. make Dockerfile
3. $ docker build . --tag extended_airflow:latest
4. make changes in yaml: image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.2} to image: ${AIRFLOW_IMAGE_NAME:-extended_airflow:latest}
5. write test dag
6. $ docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler 

