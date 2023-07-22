#!/usr/bin/env bash
air_module_path="/home/rusttm/PycharmProjects/CAP/AIR/airhome"
air_venv_path="/home/rusttm/PycharmProjects/CAP/AIR/air_ubuntu_env"
#air_cap_path="${module_path}/ModALUpdaters/ModALUpdater.py"
echo "hi everybody"
echo "Script executed from: ${PWD}"
echo "$1 updates requested"


echo "$air_module_path"
if [ -d "$air_module_path" ] && [ -d "$air_venv_path" ]; then
    echo "Directory exists, start airflow"
    set -e
    export AIRFLOW_HOME=$air_module_path
    ${air_venv_path}/bin/airflow webserver -p 8081 -D
    ${air_venv_path}/bin/airflow scheduler


else
    echo "Directory $air_module_path or $air_venv_path does not exist"
    exit 77
fi