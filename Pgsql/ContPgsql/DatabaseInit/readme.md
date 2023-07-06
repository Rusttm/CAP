in this folder placed classes for initiating new pgsql bases it:
1. sql_crt = 1 in tables_dict.json
2. ContPgsqlCreateFieldsTable.py creates field table from json file
3. ContPgsqlDataFieldsTable.py puts in db tables with fields descriptions they are creating from json files in config
4. ContPgsqlCreateReportsTable.py creates report data tables with fields and types from fields tables in db
5. ContPgsqlDataReportsTable.py fills data tables from MoiSklad module by api requests
6. data for creation stored in config folder