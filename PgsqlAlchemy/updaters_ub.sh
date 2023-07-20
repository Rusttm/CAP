#!/usr/bin/env bash
module_path="/opt/airflow/CAP/PgsqlAlchemy"
#module_path="/home/rusttm/PycharmProjects/CAP/PgsqlAlchemy"
air_cap_path="${module_path}/ModALUpdaters/ModALUpdater.py"
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
    set -e
    source "${module_path}/alch_env/bin/activate"
    python3 -u "${module_path}/ModALUpdaters/ModALTestVersion.py" $1
    deactivate
else
    echo "File $air_cap_path does not exist"
    exit 77
fi