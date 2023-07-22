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
from airflow.providers.slack.operators.slack import SlackAPIPostOperator

from airflow.hooks.base_hook import BaseHook

default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "test_slack_v6"

def get_text_4slack():
    return f"information from airflow for bot: time.now {datetime.now().strftime('%y:%m:%d %H:%M:%S')}"

def get_token() -> tuple:
    import configparser
    try:
        conf = configparser.ConfigParser()
        file = os.path.dirname(os.path.dirname(__file__))
        CONF_FILE_PATH = os.path.join(file, "config", "slackconfig.ini")
        conf.read(CONF_FILE_PATH)
        print(f"!!! my cof file is {conf}")
        token = os.environ["SLACK_TOKEN"] = conf['SLACK']['slack_token']
        chat_id = os.environ["SLACK_TOKEN"] = conf['SLACK']['my_chat_id']
        print(f"!!! my slack token is {token}")
        return token, chat_id
    except Exception as e:
        print(f"!!! cant get slack data, error: {e}")
        return None, None


with DAG(default_args=default_args,
         dag_id=DAG_ID,
         tags=["example"],
         start_date=datetime(2023, 6, 26, 14, 45),
         max_active_runs=1,
         concurrency=4,
         schedule_interval=timedelta(minutes=5),  # or '@hourly'  # or '* */1 * * *' from https://crontab.guru/#0_1_*_*_*
         dagrun_timeout=timedelta(seconds=5)
         ) as dag:

    SlackAPIPostOperator(
        task_id='failure_v6',
        token=get_token()[0],
        text=get_text_4slack(),
        channel=f'#{get_token()[1]}',
        username='airflow'
    )