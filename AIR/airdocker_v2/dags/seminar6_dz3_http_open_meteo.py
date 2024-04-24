# 3. Сделайте оператор, который отправляет запрос к
# https://goweather.herokuapp.com/weather/"location"
# (вместо location используйте ваше местоположение)

# Изменено на https://api.open-meteo.com/v1/forecast?

version = 9
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
    print(f"Температура в Москве {data_dict.get('current').get('temperature_2m')}гр.C")
    return data


with DAG(dag_id=f"seminar6_dz3_open_meteo_v{version}",
         start_date=datetime(2024, 3, 11, 12),
         schedule_interval='@daily',
         catchup=False) as dag:

    http_operator = SimpleHttpOperator(
        task_id='make_http_request',
        http_conn_id='open_api',
        endpoint='/v1/forecast?latitude=55.61&longitude=37.61&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m',
        method='GET',
        data=json.dumps({"priority": 5})
    )

    task_http_sensor_check = HttpSensor(
        task_id="http_sensor_check",
        http_conn_id="open_api",
        endpoint="/v1/forecast?latitude=55.6183&longitude=37.6153&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m",
        request_params={},
        response_check=lambda response: response.status_code == 200,
        timeout=10,
        poke_interval=5,
        method='GET',
    )

    python_weather_print = PythonOperator(
        task_id=f'python_print_weather',
        python_callable=weather_print,
        provide_context=True
    )

    task_http_sensor_check >> http_operator >> python_weather_print
