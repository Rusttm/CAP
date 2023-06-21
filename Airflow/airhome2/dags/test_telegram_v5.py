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
import time
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}




from airflow import DAG
from airflow.providers.telegram.operators.telegram import TelegramOperator
ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "test_telegram_v5"
CONN_ID = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("ADMIN_TELEGRAM_ID")
print(f"? telegram token {CONN_ID}")
print(f"? telegram admin {CHAT_ID}")

def get_token(ti) -> tuple:
    import configparser
    global CONN_ID
    global CHAT_ID
    try:
        print(f"? telegram token {CONN_ID}")
        print(f"? telegram admin {CHAT_ID}")
        conf = configparser.ConfigParser()
        file = os.path.dirname(os.path.dirname(__file__))
        CONF_FILE_PATH = os.path.join(file, "config", "tgbconfig.ini")
        conf.read(CONF_FILE_PATH)
        CONN_ID = conf['TELEGRAMBOT']['token']
        os.environ["TELEGRAM_TOKEN"] = CONN_ID
        CHAT_ID = conf['TELEGRAMBOT']['my_chat_id']
        os.environ["ADMIN_TELEGRAM_ID"] = CHAT_ID
        ti.xcom_push(key='token_tg', value=CONN_ID)
        ti.xcom_push(key='admin_tg_id', value=CHAT_ID)
        # return (CONN_ID, CHAT_ID)
    except Exception as e:
        print(f"!!! cant get telegram data, error: {e}")
        # return (None, None)
    else:
        print(f"!!! telegram token {os.environ.get('TELEGRAM_TOKEN')}")
        print(f"!!! telegram admin {os.environ.get('ADMIN_TELEGRAM_ID')}")


with DAG(default_args=default_args,
         dag_id=DAG_ID,
         start_date=datetime(2023, 6, 20),
         tags=["example"],
         schedule_interval='@daily'
         ) as dag:

    # [START howto_operator_telegram]

    send_message_telegram_task = TelegramOperator(
        task_id="send_message_telegram_v5",
        telegram_conn_id="telegram_default",
        token=CONN_ID,
        chat_id=CHAT_ID,
        text=f"Hello from Airflow! {datetime.now()}",
        dag=dag
    )
    get_token = PythonOperator(
        task_id='get_token',
        python_callable=get_token
    )

    get_token >> send_message_telegram_task

    # [END howto_operator_telegram]


# from tests.system.utils import get_test_run  # noqa: E402

# Needed to run the example DAG with pytest (see: tests/system/README.md#run_via_pytest)
# test_run = get_test_run(dag)