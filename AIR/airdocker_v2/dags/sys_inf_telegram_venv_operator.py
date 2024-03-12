#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example use of Telegram operator.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.operators.python_operator import PythonVirtualenvOperator
from airflow.decorators import dag, task
from airflow.models.taskinstance import TaskInstance


# from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import sys

# part where sets env variables for correct python imports
sys.path.append('/opt/airflow/CAP')  # main path of CAP project mounts to /opt/airflow/CAP
CURRENT_DIR = os.getcwd()  # current directory is /opt/airflow
cap_dir = os.path.join(CURRENT_DIR, "CAP")
sys.path.append(cap_dir)

# DAG configuration
VERSION = 10
START_DATE = datetime(2024, 3, 12, 10, 30),  # only UTC time
ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = f"telegram_sys_info_v{VERSION}"


def telegram_on_fail(context):
    alarm_text = f"""\U0001F914: Task Failed.
             *Task*: {context.get('task_instance').task_id}
             *Dag*: {context.get('task_instance').dag_id}
             *Execution Time *: {context.get('execution_date')}
             *Exception*: {context.get('exception')}
             *Log Url*: {context.get('task_instance').log_url}
             """

    failed_alert = TelegramOperator(
        task_id=f"task_telegram_on_failure{VERSION}",
        telegram_conn_id="telegram_default",
        token=get_token()[0],
        chat_id=get_token()[1],
        text=alarm_text
    )
    return failed_alert.execute(context=context)


def python_sys_info_operator():
    import time
    import psutil
    import sqlalchemy
    now = time.ctime()
    memory_used = round(psutil.virtual_memory().used / 1073741824, 2)
    memory_msg = f"memory usage: {psutil.virtual_memory().percent}% ({memory_used})Gb"
    cpu_msg = f"cpu usage: {psutil.cpu_percent(interval=None)}%"
    info_text = f"MSI server system info\n at {now}:\n {memory_msg}\n {cpu_msg}\n"
    info_text += f"sqlalchemy_v{sqlalchemy.__version__}\n"
    info_text += f"psutil_v{psutil.__version__}\n"
    print(f"{info_text=}")
    return info_text


def get_token() -> tuple:
    import configparser
    try:
        conf = configparser.ConfigParser()
        file = os.path.dirname(os.path.dirname(__file__))
        CONF_FILE_PATH = os.path.join(file, "config", "tgbconfig.ini")
        conf.read(CONF_FILE_PATH)
        token = os.environ["TELEGRAM_TOKEN"] = conf['TELEGRAMBOT']['token']
        admin_id = os.environ["ADMIN_TELEGRAM_ID"] = conf['TELEGRAMBOT']['my_chat_id']
        return (token, admin_id)
    except Exception as e:
        print(f"!!! cant get telegram data, error: {e}")
        return (None, None)


default_args = {
    'owner': 'rusttm',
    'start_date': datetime(2024, 3, 9, 19, 30),
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'provide_context': True,
    'on_failure_callback': telegram_on_fail
}

with (DAG(default_args=default_args,
         dag_id=DAG_ID,
         tags=["example"],
         max_active_runs=1,
         concurrency=4,
         schedule_interval=timedelta(minutes=60),
         # or '@hourly'  # or '* */1 * * *' from https://crontab.guru/#0_1_*_*_*
         dagrun_timeout=timedelta(seconds=160)
         ) as dag):

    python_sys_info = PythonOperator(
        task_id=f'airflow_python_sys_info',
        python_callable=python_sys_info_operator,
        dag=dag
    )
    virtualenv_task = PythonVirtualenvOperator(
        task_id="virtualenv_sqlalchemy",
        python_callable=python_sys_info_operator,
        requirements=["SQLAlchemy==2.0.28", "psutil"],
        # requirements=["psutil==5.9.8"],
        system_site_packages=False,
        provide_context=True,
        # op_kwargs={'sys_info_text': python_sys_info_operator},
        dag=dag,
    )

    telegram_sys_info = TelegramOperator(
        task_id=f"task_telegram_sys_info_v{VERSION}",
        telegram_conn_id="telegram_default",
        token=get_token()[0],
        chat_id=get_token()[1],
        text='{{ti.xcom_pull(task_ids="airflow_python_sys_info", key="return_value")}}' +
             '{{ti.xcom_pull(task_ids="virtualenv_sqlalchemy", key="return_value")}}',
        dag=dag
    )


    [virtualenv_task, python_sys_info] >> telegram_sys_info




