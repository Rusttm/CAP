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
Example use of venv.
from https://github.com/astronomer/astro-provider-venv
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import ExternalPythonOperator, PythonVirtualenvOperator
from airflow.decorators import task

import sys

CAP_PATH = "/home/rusttm/PycharmProjects/CAP"
sys.path.append(CAP_PATH)
CURRENT_DIR = os.getcwd()
dags_dir = os.path.join(CURRENT_DIR)
sys.path.append(dags_dir)

VERSION = 2
ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = f"venv_bash_operator_v{VERSION}"


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
    'retry': 5,
    'retry_delay': timedelta(minutes=15),
    'catchup': False,
    'on_failure_callback': telegram_on_fail
}

with DAG(default_args=default_args,
         dag_id=DAG_ID,
         tags=["example"],
         start_date=datetime(2023, 7, 21, 8, 59),  # only UTC time
         max_active_runs=1,
         concurrency=4,
         schedule_interval=timedelta(minutes=60),
         # or '@hourly'  # or '* */1 * * *' from https://crontab.guru/#0_1_*_*_*
         dagrun_timeout=timedelta(seconds=60)
         ) as dag:
    send_message_telegram_task = TelegramOperator(
        task_id=f"send_tg_v{VERSION}",
        telegram_conn_id="telegram_default",
        token=get_token()[0],
        chat_id=get_token()[1],
        # text=f"at: {datetime.now().strftime('%y:%m:%d %H:%M:%S')}\n" + "{{ti.xcom_pull(task_ids='python_update_operator', key='updater_result')}}",
        text=f"at: {datetime.now().strftime('%y:%m:%d %H:%M:%S')}\n",
        dag=dag
    )


    my_command = """$pyenv /home/rusttm/PycharmProjects/CAP/PgsqlAlchemy/ModALUpdaters/ModALTestVersion.py"""
    bash_updater = BashOperator(
        task_id="bash_task",
        bash_command=my_command + " ",
        env=dict({"pyenv": "/home/rusttm/PycharmProjects/CAP/PgsqlAlchemy/alch_env/bin/python"}),
        dag=dag)


