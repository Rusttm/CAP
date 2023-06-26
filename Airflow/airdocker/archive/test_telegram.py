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


default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'schedule_interval': '@hourly'  # or '0 * * * *' from https://crontab.guru/#0_1_*_*_*
}

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "test_telegram_v0"

def get_text_4tgbot():
    return f"information for bot: time.now {datetime.now().strftime('%y:%m:%d %H:%M:%S')}"

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
         start_date=datetime(2023, 6, 20),
         tags=["example"]
         ) as dag:

    send_message_telegram_task = TelegramOperator(
        task_id="task_send_message_telegram_v0",
        telegram_conn_id="telegram_default",
        token=get_token()[0],
        chat_id=get_token()[1],
        text=get_text_4tgbot(),
        dag=dag
    )
