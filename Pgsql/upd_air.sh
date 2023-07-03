#!/bin/bash
#!/opt/airflow/CAP/cap_env/bin python
set -e
#cd "/opt/airflow/CAP"
source "/opt/airflow/CAP/cap_env/bin/activate"
python -V
python /opt/airflow/CAP/Pgsql/run_bash_updater.py
python -V
#/opt/airflow/CAP/cap_env/bin/python /opt/airflow/Pgsql/run_bash_updater.py

