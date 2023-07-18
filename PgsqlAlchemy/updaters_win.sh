#!/bin/bash
# cap_path="C:\\Users\\User\\Desktop\\CAP\\CAP\\PgsqlAlchemy\\ModALUpdaters\\ModALUpdater.py"
cap_path="./ModALUpdaters/ModALUpdater.py"
air_cap_path="/opt/airflow/CAP/PgsqlAlchemy/ModALUpdaters/ModALUpdater.py"
echo "hi everybody"
echo "Script executed from: ${PWD}"
echo "$1 updates requested"
# echo "$cap_path"
# if [ -f "$cap_path" ]; then
#     echo "File exists, start updates"
#     ./alchemy_env/Scripts/python.exe ./ModALUpdaters/ModALUpdater.py $1
# else
#     echo "File $cap_path does not exist"
#     exit 1
# fi

echo "$air_cap_path"
if [ -f "$air_cap_path" ]; then
    echo "File exists, start updates"
    /opt/airflow/CAP/PgsqlAlchemy/alchemy_env/Scripts/python.exe /opt/airflow/CAP/PgsqlAlchemy/ModALUpdaters/ModALUpdater.py $1
else
    echo "File $air_cap_path does not exist"
    exit 1
fi