#!/bin/bash
#!/opt/airflow/CAP/cap_env/bin python
set -e
#cd "/opt/airflow/CAP"
source "../web_env/bin/activate"
python manage.py runserver 192.168.1.103:8083
