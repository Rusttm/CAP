#!/bin/bash
# cap_path="C:\\Users\\User\\Desktop\\CAP\\CAP\\PgsqlAlchemy\\ModALUpdaters\\ModALUpdater.py"
cap_path="./ModALUpdaters/ModALUpdater.py"
echo "hi everybody"
echo "$1"
echo "$cap_path"
if [ -f "$cap_path" ]; then
    echo "File exists, start updates"
    ./alchemy_env/Scripts/python.exe ./ModALUpdaters/ModALUpdater.py $1
else
    echo "File $cap_path does not exist"
fi
