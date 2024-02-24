#!/usr/bin/env bash
module_path="/home/rusttm/PycharmProjects/CAP"
#module_path="/home/rusttm/PycharmProjects/CAP/PgsqlAlchemy"
cap_path="${module_path}/CAPMain/Start.py"
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

echo "$cap_path"
if [ -f "$cap_path" ]; then
    echo "File exists, start cap main module"
    set -e
    export PYTHONPATH="${PYTHONPATH}:/home/rusttm/PycharmProjects/CAP/"
    source "${module_path}/cap_env/bin/activate"
    python3 -u "${module_path}/CAPMain/Start.py" $1
    deactivate
else
    echo "File $cap_path does not exist"
    exit 77
fi