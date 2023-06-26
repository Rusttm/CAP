FROM apache/airflow:latest-python3.10
COPY requirements.txt /opt/airflow/config/requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /opt/airflow/config/requirements.txt