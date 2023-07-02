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
from airflow.operators.python import PythonOperator
from airflow import DAG
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.operators.bash_operator import BashOperator

import sys

# sys.path.append('/home/rusttm/PycharmProjects/CAP/Pgsql')
CURRENT_DIR = os.getcwd()
cap_dir = os.path.join(CURRENT_DIR, "CAP")
sys.path.append(cap_dir)


# from Pgsql.PgsqlUpdaterAir import PgsqlUpdaterAir

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


default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'on_failure_callback': telegram_on_fail
}
VERSION = 9
ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = f"test_updater_v{VERSION}"


def get_text_4tgbot():
    import platform
    # from Pgsql.PgsqlUpdaterAir import PgsqlUpdaterAir
    text_line = ""
    CURRENT_DIR = os.getcwd()
    cap_dir = os.path.join(CURRENT_DIR, "CAP")
    sys.path.append(cap_dir)
    text_line += "///".join(os.listdir(cap_dir))
    sys_os = platform.platform()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # os.environ['PATH'] += ':' + dir_path
    # sys.path.insert(0, dir_path)
    # sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    text_line += f"Current project path: {dir_path} added to System: {sys_os}, system paths {sys.path}"
    text_line += f"information from airflow for bot: time.now {datetime.now().strftime('%y:%m:%d %H:%M:%S')}"
    # print(os.path.realpath(__file__))
    text_line += os.path.realpath(__file__)
    return text_line


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


with DAG(default_args=default_args,
         dag_id=DAG_ID,
         tags=["example"],
         start_date=datetime(2023, 7, 2, 14, 50),  # only UTC time
         max_active_runs=1,
         concurrency=4,
         schedule_interval=timedelta(minutes=5),
         # or '@hourly'  # or '* */1 * * *' from https://crontab.guru/#0_1_*_*_*
         dagrun_timeout=timedelta(seconds=60)
         ) as dag:

    send_message_telegram_task = TelegramOperator(
        task_id=f"task_update_db_v{VERSION}",
        telegram_conn_id="telegram_default",
        token=get_token()[0],
        chat_id=get_token()[1],
        text=get_text_4tgbot(),
        dag=dag
    )

    task_updater = BashOperator(
        task_id="bash_task_updater",
        bash_command="./upd_air_test.sh",
        # bash_command="/opt/airflow/CAP/cap_env/bin/python",
        dag=dag)

    task_updater >> send_message_telegram_task
