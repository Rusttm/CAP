# 3. Сделайте оператор, который отправляет запрос к
# https://goweather.herokuapp.com/weather/"location"
# (вместо location используйте ваше местоположение)

version = 10
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.bash import BashOperator
from datetime import datetime
import json


def weather_print(**context):
    data = context['task_instance'].xcom_pull(task_ids='make_http_request')
    data_dict = json.loads(data)
    print(f"Температура в Москве {data_dict.get('temperature')}")
    return data


with DAG(dag_id=f"seminar6_dz3_heroku_v{version}",
         start_date=datetime(2024, 3, 11, 12),
         schedule_interval='@daily',
         catchup=False) as dag:
    http_operator = SimpleHttpOperator(
        task_id='make_http_request',
        http_conn_id='weather_api',
        endpoint='/weather/Moscow',
        method='GET',
        data=json.dumps({"priority": 5})
    )

    python_weather_print = PythonOperator(
        task_id=f'python_print_weather',
        python_callable=weather_print,
        provide_context=True
    )

    http_operator >> python_weather_print
