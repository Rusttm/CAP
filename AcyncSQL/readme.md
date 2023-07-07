This module for async generate report tables from existing tables

1. **GenASQLCreateBalTable.py** Creates table in empty base: gets inn from customer_table 
and creates columns names like inn_7564385 also check if its already exist (create only new cols)

2. **GenASQLFulFillBalTable.py** takes data from tables (**ContASQLGetData4Bal.py**) and puts them in table

3.