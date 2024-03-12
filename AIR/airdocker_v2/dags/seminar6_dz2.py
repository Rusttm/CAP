# 2. Создайте PythonOperator, который генерирует рандомное число,
# возводит его в квадрат и выводит в консоль исходное число и результат.

version = 1
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from random import randint

def random_sq():
    number = randint(5, 50)
    result = number ** 2
    print(f"{number=}, square is {result=}")
    return number, result

with DAG(dag_id=f"seminar6_dz2_v{version}", start_date=datetime(2024, 3 ,11, 12),
         schedule_interval='@daily',
         catchup=False) as dag:
    training_model_tasks = PythonOperator(
        task_id=f"python_op_random",
        python_callable=random_sq)

