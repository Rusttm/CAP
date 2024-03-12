# 1. Создайте новый граф. Добавьте в него BashOperator,
# который будет генерировать рандомное число и печатать его в
# консоль.
#
# 2. Создайте PythonOperator, который генерирует рандомное число,
# возводит его в квадрат и выводит в консоль исходное число и результат.
#
# 3. Сделайте оператор, который отправляет запрос к
# https://goweather.herokuapp.com/weather/"location" (вместо location используйте ваше местоположение).
#
# 4. Задайте последовательный порядок выполнения операторов.

version = 11
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.bash import BashOperator
from datetime import datetime
import json
from random import randint


def random_sq():
    number = randint(5, 50)
    result = number ** 2
    print(f"{number=}, square is {result=}")
    return number, result


def weather_print(**context):
    data = context['task_instance'].xcom_pull(task_ids='make_http_request')
    data_dict = json.loads(data)
    print(f"Температура в Москве {data_dict.get('temperature')}")
    return data


with DAG(dag_id=f"seminar6_dz4_v{version}",
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

    bash_operator = BashOperator(
        task_id="bash_operator",
        bash_command="PORT=$((((RANDOM<<15)|RANDOM) % 63001 + 2000 )) && echo 'Random int value is:' ${PORT}"
    )

    python_randint = PythonOperator(
        task_id=f"python_op_random",
        python_callable=random_sq)

    bash_operator >> python_randint >> http_operator >> python_weather_print
