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
from airflow.operators.bash_operator import BashOperator
from airflow.hooks.base_hook import BaseHook

# from https://www.reply.com/data-reply/en/content/integrating-slack-alerts-in-airflow

SLACK_CONN_ID = 'my_airflow'


def slack_failed_task_v1(context):
    """
    gets data from airflow connection
    Sends message to a slack channel .
    If you want to send it to a "user" -> use "@user",
        if "public channel" -> use "#channel",
        if "private channel" -> use "channel"
    """
    slack_channel = BaseHook.get_connection(SLACK_CONN_ID).description
    slack_token = BaseHook.get_connection(SLACK_CONN_ID).password
    failed_alert = SlackAPIPostOperator(
        task_id='slack_failed',
        channel=slack_channel,
        token=slack_token,
        text="""
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            ti=context.get('task_instance'),
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
        )
    )
    return failed_alert.execute(context=context)


def slack_failed_task_v2(context):
    """ gets data from config file"""
    failed_alert = SlackAPIPostOperator(
        task_id='slack_failed_simple',
        channel=f'#{get_token()[1]}',
        token=get_token()[0],
        text=f":red_circle: Task Failed at {datetime.now().strftime('%y:%m:%d %H:%M:%S')} information: {get_text_4slack()}",
        username='airflow')
    return failed_alert.execute(context=context)


default_args = {
    'owner': 'rusttm',
    'retry': 5,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'on_failure_callback': slack_failed_task_v1
}

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "test_bash_slack_v1"


def get_text_4slack():
    text = f"information from airflow for bot: time.now {datetime.now().strftime('%y:%m:%d %H:%M:%S')}"
    return text


def get_token() -> tuple:
    import configparser
    try:
        conf = configparser.ConfigParser()
        file = os.path.dirname(os.path.dirname(__file__))
        CONF_FILE_PATH = os.path.join(file, "config", "slackconfig.ini")
        conf.read(CONF_FILE_PATH)
        token = os.environ["SLACK_TOKEN"] = conf['SLACK']['slack_token']
        chat_id = os.environ["SLACK_TOKEN"] = conf['SLACK']['my_chat_id']
        # print(f"!!! my configuration is: {BaseHook.get_connection(SLACK_CONN_ID).password}")
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
         schedule_interval=timedelta(minutes=5),
         # or '@hourly'  # or '* */1 * * *' from https://crontab.guru/#0_1_*_*_*
         dagrun_timeout=timedelta(seconds=60)
         ) as dag:
    task_with_failed_slack_alerts = BashOperator(
        task_id="fail_bash_task",
        bash_command="exit 1",
        dag=dag)
