import datetime

from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
from AcyncSQL.ConnASQL.ConnASQLDataGet import ConnASQLDataGet
import sqlalchemy
import pandas.io.sql as pd_psql
import pandas as pd
import asyncio
import asyncpg
import json

class ConnASQLDataGet4Bal(ConnASQLMainClass):
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

    async def get_col_data_from_table_inn(self, **kwargs) -> list:
        table_name: str = None
        col_list: list = None
        from_date: str = None
        to_date: str = None
        to_file: bool = False
        """returns list of transactions"""
        table_name = kwargs.get('table_name', None)
        col_list = kwargs.get('col_list', None)
        to_file = kwargs.get('to_file', False)
        _conn = await asyncpg.connect(**self.__config_dict)
        col_line = ",".join(col_list)
        req_line = f"SELECT {col_line} FROM {table_name}"
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        result_dict = dict()
        for customer_href, customer_inn in table_data:

            customer_href_dict = json.loads(customer_href)
            customer_meta = dict({"meta": customer_href_dict})
            print(customer_meta)
            # result_dict.update({customer_meta: customer_inn})

        if to_file:
            pd_data = pd.DataFrame.from_records(table_data, columns=col_list)
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return result_dict

    async def get_col_data_from_table_date_filtered_bal(self, **kwargs) -> list:
        table_name: str = None
        col_list: list = None
        from_date: str = None
        to_date: str = None
        to_file: bool = False
        """returns list of transactions"""
        table_name = kwargs.get('table_name', None)
        col_list = kwargs.get('col_list', None)
        date_col = kwargs.get('date_col', None)
        from_date = kwargs.get('from_date', self.left_date)
        to_date = kwargs.get('to_date', datetime.datetime.now())
        factor = kwargs.get('factor', 1)
        to_file = kwargs.get('to_file', False)
        _conn = await asyncpg.connect(**self.__config_dict)
        col_line = ",".join(col_list)
        req_line = f"SELECT {col_line} FROM {table_name} WHERE {date_col} >= '{from_date}' AND {date_col} <= '{to_date}'"
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        result_list = []
        for agent_meta, doc_sum, doc_date in table_data:
            result_list.append((doc_date, json.loads(agent_meta), factor * doc_sum / 100))
        excell_conn = None
        if to_file:
            pd_data = pd.DataFrame.from_records(table_data, columns=col_list)
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return result_list


if __name__ == '__main__':
    connector = ConnASQLDataGet4Bal()
    loop = asyncio.new_event_loop()
    # loop.run_until_complete(connector.test_connection())
    # data = loop.run_until_complete(connector.get_all_data_from_table_with_path('pgsql_service_fields', to_file=True))
    # print(data)
    req_dict = {
        'table_name': 'payments_in_table',
        'col_list': ['agent', 'sum', 'created'],
        'date_col': 'created',
        'from_date': '2023-06-01 00:00:00',
        'to_date': '2023-07-01 23:59:59',
        'factor': 1,
        'to_file': True,
    }

    task1 = connector.get_col_data_from_table_date_filtered_bal(**req_dict)

    # loop.run_until_complete(connector.get_all_data_from_table('payments_in_table', to_file=True))
    # print(connector.create_connection())
    # print(connector.close_connection())
    req_dict2 = {
        'table_name': 'customers_table',
        'col_list': ['meta', 'inn'],
        'to_file': True,
    }
    task2 = connector.get_col_data_from_table_inn(**req_dict2)
    data = loop.run_until_complete(task2)
    print(data)

    # print(connector.get_all_tables_list())
    # print(connector.get_pd_from_table(table_name='payments_out_table', to_file=True))
    # print(connector.get_pd_from_table(table_name='pgsql_service_fields', to_file=True))
    print("finish")