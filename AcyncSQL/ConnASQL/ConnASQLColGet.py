from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
import sqlalchemy
import pandas.io.sql as pd_psql
import pandas as pd
import asyncio
import asyncpg

class ConnASQLDataGet(ConnASQLMainClass):
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


    async def get_table_col_names(self, table_name) -> list:
        _conn = await asyncpg.connect(**self.__config_dict)
        req_line = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';"
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        pd_data = pd.DataFrame.from_records(table_data)
        col_list = list(pd_data[0])
        return col_list



if __name__ == '__main__':
    connector = ConnASQLDataGet()
    loop = asyncio.new_event_loop()
    req_dict = {
        'table_name': 'payments_in_table'
    }

    task1 = connector.get_table_col_names(**req_dict)
    data = loop.run_until_complete(task1)
    print(data)
    print("finish")