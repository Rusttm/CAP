# this dockerfile creates base image with additional libraries for airflow in docker
# $ docker build . --tag extended_airflow:latest
# FROM apache/airflow:latest-python3.10
FROM apache/airflow:2.8.2-python3.10
# install additional libraries for dags
COPY requirements.txt /opt/airflow/config/requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /opt/airflow/config/requirements.txt

