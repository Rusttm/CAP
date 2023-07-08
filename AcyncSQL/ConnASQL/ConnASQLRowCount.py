from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
import pandas as pd
import asyncio
import asyncpg

class ConnASQLRowCount(ConnASQLMainClass):
    _conn = None
    __config_dict = dict()

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


    async def get_table_row_num(self, table_name) -> list:
        try:
            _conn = await asyncpg.connect(**self.__config_dict)
            req_line = f"SELECT COUNT(position_id) FROM {table_name} ;"
            table_data = await _conn.fetch(req_line)
            await _conn.close()
            pd_data = pd.DataFrame.from_records(table_data)
            row_num = list(pd_data[0])
            return row_num[0]
        except Exception as e:
            error_msg = f" cant get row numbers in table {table_name}, error: {e}"
            print(error_msg)
            self.logger.error(error_msg)
            return 0
    def non_async_get_table_row_num(self, table_name):

        res = asyncio.run(self.get_table_row_num(table_name=table_name))
        return res







if __name__ == '__main__':
    connector = ConnASQLRowCount()
    loop = asyncio.new_event_loop()
    req_dict = {
        'table_name': 'payments_in_table'
    }

    task1 = connector.get_table_row_num(**req_dict)
    data = loop.run_until_complete(task1)
    print(data)
    print("finish")

    print(connector.non_async_get_table_row_num(**req_dict))