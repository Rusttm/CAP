from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}

def get_sklearn_version():
    import sklearn
    print(f"aiogram version is {sklearn.__version__}")


with DAG(
    default_args=default_args,
    dag_id='test_sklearn_version',
    start_date=datetime(2023,6, 21),
    schedule_interval='@daily'
) as dag:
    get_sklearn_version = PythonOperator(
        task_id='sklearn_version',
        python_callable=get_sklearn_version
    )
    get_sklearn_version