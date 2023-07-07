import datetime

from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
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

    async def get_col_data_from_table(self, **kwargs) -> pd.DataFrame:
        """ get data"""
        table_name = kwargs.get('table_name', None)
        col_list = kwargs.get('col_list', None)
        _conn = await asyncpg.connect(**self.__config_dict)
        col_line = ",".join(col_list)
        req_line = f"SELECT {col_line} FROM {table_name}"
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        pd_data = pd.DataFrame.from_records(table_data, columns=col_list)
        return pd_data

    async def get_col_data_from_table_inn(self, **kwargs) -> dict:
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
        for customer_meta, customer_inn in table_data:
            customer_href = json.loads(customer_meta)
            result_dict.update({customer_href["href"]: customer_inn})

        if to_file:
            pd_data = pd.DataFrame.from_records(table_data, columns=col_list)
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return result_dict

    async def get_col_data_from_table_id(self, **kwargs) -> dict:
        table_name: str = None
        col_list: list = None
        from_date: str = None
        to_date: str = None
        to_file: bool = False
        """returns dict {href: id}"""
        table_name = kwargs.get('table_name', None)
        col_list = kwargs.get('col_list', None)
        to_file = kwargs.get('to_file', False)
        _conn = await asyncpg.connect(**self.__config_dict)
        col_line = ",".join(col_list)
        req_line = f"SELECT {col_line} FROM {table_name}"
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        result_dict = dict()
        for customer_meta, customer_inn in table_data:
            customer_href = json.loads(customer_meta)
            customer_id = customer_href["href"].split("/")[-1]
            result_dict.update({customer_href["href"]: customer_id})

        if to_file:
            pd_data = pd.DataFrame.from_records(table_data, columns=col_list)
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
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
            customer_meta = json.loads(agent_meta)
            result_list.append((doc_date, customer_meta["meta"]["href"], factor * doc_sum / 100))
        excell_conn = None
        if to_file:
            pd_data = pd.DataFrame.from_records(table_data, columns=col_list)
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return result_list

    async def get_last_row_in_table_pd(self, **kwargs) -> dict:
        table_name = kwargs.get('table_name', None)
        """returns last row in table"""
        req_line = f"SELECT position_id FROM {table_name} ORDER BY position_id DESC LIMIT 1;"
        _conn = await asyncpg.connect(**self.__config_dict)
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        pd_data = pd.DataFrame.from_records(table_data)
        condition = pd_data[0][0]
        req_line = f"SELECT * FROM {table_name} WHERE position_id = {condition} LIMIT 1;"
        _conn = await asyncpg.connect(**self.__config_dict)
        # await _conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema='pg_catalog')
        asyncpg_record = await _conn.fetch(req_line)
        await _conn.close()
        res_dict = [dict(row) for row in asyncpg_record]
        return res_dict[0]


if __name__ == '__main__':
    connector = ConnASQLDataGet4Bal()
    loop = asyncio.new_event_loop()
    req_dict1 = {
        'table_name': 'payments_in_table',
        'col_list': ['agent', 'sum', 'created'],
        'date_col': 'created',
        'from_date': '2023-07-07 00:00:00.000',
        'to_date': '2023-07-07 23:59:59.000',
        'factor': 1,
        'to_file': True,
    }
    task1 = connector.get_col_data_from_table_date_filtered_bal(**req_dict1)

    # request inn dictionary
    req_dict2 = {
        'table_name': 'customers_table',
        'col_list': ['meta', 'inn'],
        'to_file': True,
    }
    task2 = connector.get_col_data_from_table_inn(**req_dict2)
    task3 = connector.get_col_data_from_table_id(**req_dict2)
    req_dict4 = {
        'table_name': 'customers_daily_bal_table',
    }
    task4 = connector.get_last_row_in_table_pd(**req_dict4)

    req_dict5 = {
        'table_name': 'customers_bal_table',
        'col_list': ['meta', 'balance'],
    }
    task5 = connector.get_col_data_from_table(**req_dict5)

    # print(f"number of transactions {len(transaction_list)}")
    # result_list = [(tr_date, href_dict.get(href, None), tr_sum) for tr_date, href, tr_sum in transaction_list]
    data = loop.run_until_complete(task5)
    loop.close()
    print(data)

    print("finish")