from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}

def get_aiogram_version():
    import aiogram
    print(f"aiogram version is {aiogram.__version__}")


with DAG(
    default_args=default_args,
    dag_id='test_aiogram_version',
    start_date=datetime(2023,6, 21),
    schedule_interval='@daily'
) as dag:
    get_aiogram_version = PythonOperator(
        task_id='aiogram_version',
        python_callable=get_aiogram_version
    )
    get_aiogram_version