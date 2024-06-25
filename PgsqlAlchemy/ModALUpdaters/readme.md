if you want to add table for updater:
1. Three types of update in file ModALUpdater:
   2. Hourly
   3. Daily

1. make model json file and pu it in config/models
2. prepare model json file in ModALGetModFromJson, this handle your json file
3. add "updated", "req_func", "date_field", "config_url", "unique_col", "updated" 
4. make from this json model file.py in ModALMakeModFile and run it

if you use VSCODE windows
from https://stackoverflow.com/questions/62366211/vscode-modulenotfounderror-no-module-named-x

1. Press Ctrl + Shift + P to open Command Palette
2. Go to Users.setting.json
3. Add the following line


"terminal.integrated.env.windows": { "PYTHONPATH": "${C:\\Users\\User\\Desktop\\CAP\\CAP}" }