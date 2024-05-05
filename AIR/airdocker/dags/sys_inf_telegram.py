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
import psutil
import time
# from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import sys

# part where sets env variables for correct python imports
sys.path.append('/opt/airflow/CAP')  # main path of CAP project mounts to /opt/airflow/CAP
CURRENT_DIR = os.getcwd()  # current directory is /opt/airflow
cap_dir = os.path.join(CURRENT_DIR, "CAP")
sys.path.append(cap_dir)

# DAG configuration
VERSION = 1
START_DATE = datetime(2023, 7, 5, 19, 30),  # only UTC time
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


def telegram_sys_info(context):
    ti = context['ti']
    sys_info_text = f"{ti.xcom_pull(task_ids='python_sys_info', key='sys_info_result')}"
    send_sys_info = TelegramOperator(
        task_id=f"task_telegram_sys_info_v{VERSION}",
        telegram_conn_id="telegram_default",
        token=get_token()[0],
        chat_id=get_token()[1],
        text=sys_info_text,
        dag=dag
    )
    return send_sys_info.execute(context=context)


def python_sys_info_operator(**kwargs):
    """ prepare information for telegram"""
    now = time.ctime()
    memory_used = round(psutil.virtual_memory().used / 1073741824, 2)
    memory_msg = f"memory usage: {psutil.virtual_memory().percent}% ({memory_used})Gb"
    cpu_msg = f"cpu usage: {psutil.cpu_percent(interval=None)}%"
    info_text = f"MSI server system info\n at {now}:\n {memory_msg}\n {cpu_msg}"
    ti = kwargs['ti']
    # put this information to xcom
    ti.xcom_push(key='sys_info_result', value=info_text)
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
    'start_date': datetime(2023, 7, 5, 19, 30),
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'on_failure_callback': telegram_on_fail,
    'on_success_callback': telegram_sys_info
}

with DAG(default_args=default_args,
         dag_id=DAG_ID,
         tags=["example"],
         max_active_runs=1,
         concurrency=4,
         schedule_interval=timedelta(minutes=60),
         # or '@hourly'  # or '* */1 * * *' from https://crontab.guru/#0_1_*_*_*
         dagrun_timeout=timedelta(seconds=60)
         ) as dag:

    python_sys_info = PythonOperator(
        task_id=f'python_sys_info',
        python_callable=python_sys_info_operator,
        dag=dag
    )
    # send_message_telegram_task = TelegramOperator(
    #     task_id=f"send_tg_sys_info_v{VERSION}",
    #     telegram_conn_id="telegram_default",
    #     token=get_token()[0],
    #     chat_id=get_token()[1],
    #     text=f"at: {datetime.now().strftime('%y:%m:%d %H:%M:%S')}\n" + "{{ti.xcom_pull(task_ids='python_update_operator', key='updater_result')}}",
    #     dag=dag
    # )
    #
    # bash_updater = BashOperator(
    #     task_id="bash_task_updater",
    #     bash_command="./upd_air_test.sh",
    #     dag=dag)



