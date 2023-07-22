import os

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "example_telegram"
CONN_ID = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = "731370983"
print(CONN_ID)