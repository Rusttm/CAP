if you want to add table for updater:

1. make model json file and pu it in config/models
2. prepare model json file in ModALGetModFromJson, this handle your json file
3. add "updated", "req_func", "date_field", "config_url", "unique_col", "updated" 
4. make from this json model file.py in ModALMakeModFile and run it