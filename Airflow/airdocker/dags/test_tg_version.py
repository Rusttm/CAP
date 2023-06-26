from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator



default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}

def get_tg_version():
    # import airflow.providers.telegram.operators
    from platform import python_version
    print(f"Python version {python_version()}")
    print(f"Python unknown Airflow")


with DAG(
    default_args=default_args,
    dag_id='test_tg_version',
    start_date=datetime(2023, 6, 20),
    schedule_interval='@daily'
) as dag:
    get_sklearn_version = PythonOperator(
        task_id='sklearn_version',
        python_callable=get_tg_version
    )
