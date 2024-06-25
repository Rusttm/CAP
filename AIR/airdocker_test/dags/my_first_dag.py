from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
import logging

def print_hello():
    logging.info('Hello, Rustam!')
    return 'Hello, Rustam, from first Airflow DAG!'

dag = DAG('my_first_dag', description='Hello World DAG',
          schedule_interval='0 1 * * *',
          start_date=datetime(2024, 4, 24, 12, 0), catchup=False)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)
