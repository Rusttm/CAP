import datetime

from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
import pandas as pd
import asyncio
import asyncpg
import json
import re

class ConnASQLDataPut(ConnASQLMainClass):
    _conn = None
    __config_dict = dict()
    left_date = datetime.datetime(2018, 1, 1)

    def __init__(self):
        super().__init__()
        self.__config_dict = self.get_conn_dict()

    async def test_connection(self):
        try:
            self._conn = await asyncpg.connect(**self.__config_dict)
            print("connection established")
            await self._conn.close()
            return True
        except Exception as e:
            print(f"connection cannot be established, error {e}")
            self.logger.warning(f"{__class__.__name__} cant create new connection error: {e}")
            return False

    async def put_data_to_table(self, **kwargs) -> dict:
        table_name = kwargs.get('table_name', None)
        col_list = kwargs.get('col_list', None)
        val_list = kwargs.get('val_list', None)
        _conn = await asyncpg.connect(**self.__config_dict)
        req_line = f"INSERT INTO {table_name} ({','.join(col_list)}) VALUES ('{','.join(val_list)}')"
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        return True

    async def put_data_to_table_with_date(self, **kwargs) -> bool:
        table_name = kwargs.get('table_name', None)
        col_list = kwargs.get('col_list', None)
        val_list = kwargs.get('val_list', None)
        # date_search = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", val_list[0])
        # time_search = re.search("([0-9]{2}\:[0-9]{2}\:[0-9]{2})", val_list[0])
        values_tuple = tuple(val_list)
        req_line = f"INSERT INTO {table_name} ({', '.join(col_list)}) VALUES {values_tuple}"

        try:
            _conn = await asyncpg.connect(**self.__config_dict)
            table_data = await _conn.fetch(req_line)
            await _conn.close()
        except asyncpg.exceptions.UniqueViolationError as e:
            error_line = f"row insertion cancelled, unique value already exist, error: {e}"
            print(error_line)
            self.logger.error(error_line)
            return False
        return True



if __name__ == '__main__':
    connector = ConnASQLDataPut()
    loop = asyncio.new_event_loop()
    req_dict1 = {
        'table_name': 'customers_daily_bal_table',
        'col_list': ['bal_on_date'],
        'val_list': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
    }
    task1 = connector.put_data_to_table(**req_dict1)
    data = loop.run_until_complete(task1)
    loop.close()
    print(data)
    print("finish")