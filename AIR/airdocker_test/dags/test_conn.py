import datetime
import pendulum
import os
import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models.connection import Connection
import json
from airflow.operators.python_operator import PythonOperator

@dag(
    dag_id="test_connection_v8",
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2024, 4, 24, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def TestConnection():

    @task
    def make_connection():
        test_connection = Connection(
            conn_id="postgres_conn2",
            conn_type="Postgres",
            description="connection description",
            host="172.17.0.0",
            login="test_user",
            password="testuser_pass",
            extra=json.dumps(dict(this_param="some val", that_param="other val*")),
        )

        print(f"AIRFLOW_CONN_{test_connection.conn_id.upper()}='{test_connection.as_json()}'")

    make_connection

dag = TestConnection()