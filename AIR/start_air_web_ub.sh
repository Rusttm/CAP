#!/usr/bin/env bash
air_module_path="/home/rusttm/PycharmProjects/CAP/AIR/airhome"
air_venv_path="/home/rusttm/PycharmProjects/CAP/AIR/air_ubuntu_env"
echo "Checking airhome and venv"
echo "Script executed from: ${PWD}"
echo "$1 command doesnt exist"


echo "$air_module_path"
if [ -d "$air_module_path" ] && [ -d "$air_venv_path" ]; then
    echo "Directory exists, start airflow webserver"
    set -e
    source ${air_venv_path}/bin/activate
    export AIRFLOW_HOME=$air_module_path
    airflow webserver -p 8081

else
    echo "Directory $air_module_path or $air_venv_path does not exist"
    exit 77
fi