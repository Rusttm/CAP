# 1. Создайте новый граф. Добавьте в него BashOperator,
# который будет генерировать рандомное число и печатать его в
# консоль

version = 3
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from random import randint


with DAG(dag_id=f"seminar6_dz1_v{version}", start_date=datetime(2024, 3 ,11, 12),
         schedule_interval='@daily',
         catchup=False) as dag:
    bash_operator = BashOperator(
        task_id="bash_operator",
        bash_command="PORT=$((((RANDOM<<15)|RANDOM) % 63001 + 2000 )) && echo 'Random int value is:' ${PORT}"
        )

