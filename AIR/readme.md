New test module for scheduling updates


* Instalation with in venv 
working directory /Users/johnlennon/RusttmGDrive/Python/CAP/Airflow/airhome* 
* venv air_env
from https://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html:
1. $ pip freeze | xargs pip uninstall -y
2. $ pip install "apache-airflow==2.6.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.2/constraints-3.7.txt"
   2.1 $ pip install "apache-airflow[celery]==2.5.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.5.3/constraints-3.10.txt"
   2.2 $ pip install "apache-airflow==2.6.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.3/constraints-3.10.txt"
3. $ pip3 freeze > requirements.txt
4. $ source air_ubuntu_env/bin/activate
5. $ pip install -r air_requirements.txt
6. $ export AIRFLOW_HOME=/Users/johnlennon/RusttmGDrive/Python/CAP/AIR/airhome
   3.1 $ export AIRFLOW_HOME=/home/rusttm/PycharmProjects/CAP/AIR/airhome
   3.2 if you want to change sqlite to postgresql read https://betterdatascience.com/apache-airflow-parallelism/ and change in airflow.cfg
      3.2.1 sql_alchemy_conn = postgresql+psycopg2://<user>:<user_pass>@<host>/<db>
      3.2.2. executor = LocalExecutor
7. $ airflow db init 
8. $ airflow webserver -p 8081
9. $ airflow users create  --username root --firstname firstname --lastname lastname --role Admin --email rustammazhatov@gmail.com
in new terminal
10. $ export AIRFLOW_HOME=/Users/johnlennon/RusttmGDrive/Python/CAP/AIR/airhome
11. $ airflow scheduler

# $ pip install airflow['all']
# $ pip install -r air_requirements.txt

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
   2.2 run  $ DOCKER_BUILDKIT=1 docker build .
   2.3 To use Docker BuildKit by default, edit the Docker daemon configuration in /etc/docker/daemon.json as follows, and restart the daemon ({"features": {"buildkit": true } }).
3. $ docker build . --tag extended_airflow:latest
4. make changes in yaml: image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.6.2} to image: ${AIRFLOW_IMAGE_NAME:-extended_airflow:latest}
5. write test dag
6. $ docker compose up airflow-init
# this code not works cause no postgres base
# 6. $ docker-compose up -d --no-deps --build airflow-webserver airflow-scheduler 
# 7. if changes permissions sudo chmod -R 777

Start from commandline
1. $ cd /home/rusttm/PycharmProjects/CAP/Airflow
2. $ source air_ubuntu_env/bin/activate
3. $ export AIRFLOW_HOME=/home/rusttm/PycharmProjects/CAP/Airflow/airhome2
4. $ airflow webserver -p 8081
in new terminal
5. $ export AIRFLOW_HOME=/home/rusttm/PycharmProjects/CAP/Airflow/airhome2
6. $ airflow scheduler

start .sh scripts in Ubuntu
1. $ cd ./PycharmProjects/CAP/AIR
2. $ ./start_air_web_ub.sh
3. $ ./start_air_shed_ub.sh

Issues
1. Airflow DAGs on Ubuntu machine cant find modules. 
Resolved: added at upd_func sys.path.insert(0, os.path.dirname("/home/rusttm/PycharmProjects/CAP/PgsqlAlchemy"))