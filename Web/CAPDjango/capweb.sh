#!/bin/bash
#!/opt/airflow/CAP/cap_env/bin python
set -e
#cd "/opt/airflow/CAP"
source "../web_env/bin/activate"
python manage.py runserver 127.0.0.1:8083
