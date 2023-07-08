import pandas

from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
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
            # self._conn = await asyncpg.connect(user=self.__config_dict.get("user"),
            #                                    password=self.__config_dict.get("password"),
            #                                    host=self.__config_dict.get("host"),
            #                                    database=self.__config_dict.get("database"),
            #                                    port=self.__config_dict.get("port"))
            self._conn = await asyncpg.connect(**self.__config_dict)
            print("connection established")
            await self._conn.close()
            return True
        except Exception as e:
            print(f"connection cannot be established, error {e}")
            self.logger.warning(f"{__class__.__name__} cant create new connection error: {e}")
            return False

    async def get_all_data_from_table_with_path(self, table_name: str, to_file=True) -> dict:
        """ dict({"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_conn})"""
        _conn = await asyncpg.connect(**self.__config_dict)
        table_data = await _conn.fetch(f'SELECT * FROM {table_name}')
        await _conn.close()
        columns = [col for col in table_data[0].keys()]
        # columns = [a.name for a in table_data.get_attributes()]
        pd_data = pd.DataFrame.from_records(table_data, columns=columns)
        excell_conn = None
        if to_file:
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return dict({"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_conn})

    async def get_col_data_from_table(self, table_name: str = None, col_list: list = None, to_file=True) -> dict:
        """ dict({"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_conn})"""
        _conn = await asyncpg.connect(**self.__config_dict)
        table_data = await _conn.fetch(f'SELECT {",".join(col_list)} FROM {table_name}')
        await _conn.close()
        columns = [col for col in table_data[0].keys()]
        # columns = [a.name for a in table_data.get_attributes()]
        pd_data = pd.DataFrame.from_records(table_data, columns=columns)
        excell_conn = None
        if to_file:
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return dict({"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_conn})

    async def get_col_data_from_table_pd(self, table_name: str = None, col_list: list = None, to_file=True) -> pandas.DataFrame:
        """ dict({"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_conn})"""
        _conn = await asyncpg.connect(**self.__config_dict)
        table_data = await _conn.fetch(f'SELECT {",".join(col_list)} FROM {table_name}')
        await _conn.close()
        columns = [col for col in table_data[0].keys()]
        # columns = [a.name for a in table_data.get_attributes()]
        pd_data = pd.DataFrame.from_records(table_data, columns=columns)
        excell_conn = None
        if to_file:
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return pd_data

    async def get_row_from_table_pd_json(self, **kwargs) -> pandas.DataFrame:
        """ return row """
        table_name = kwargs.get("table_name", None)
        col_name = kwargs.get("col_name", None)
        col_val = kwargs.get("col_val", None)
        _conn = await asyncpg.connect(**self.__config_dict)
        sql_string = f"SELECT * FROM {table_name} WHERE {col_name} ->> 'id' = '{col_val.get('id', None)}';"
        table_data = await _conn.fetch(sql_string)
        await _conn.close()
        pd_data = pd.DataFrame.from_records(table_data)
        return pd_data

    async def get_col_data_from_table_date_filtered(self, **kwargs) -> dict:
        table_name: str = None
        col_list: list = None
        from_date: str = None
        to_date: str = None
        to_file: bool = False
        """dict({"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_conn})"""
        table_name = kwargs.get('table_name', None)
        col_list = kwargs.get('col_list', None)
        date_col = kwargs.get('date_col', None)
        from_date = kwargs.get('from_date', None)
        to_date = kwargs.get('to_date', None)
        to_file = kwargs.get('to_file', False)
        factor = kwargs.get('factor', 1)
        _conn = await asyncpg.connect(**self.__config_dict)
        col_line = ",".join(col_list)
        req_line = f"SELECT {col_line} FROM {table_name} WHERE {date_col} >= '{from_date}' AND {date_col} <= '{to_date}'"
        table_data = await _conn.fetch(req_line)
        await _conn.close()
        # columns = [col for col in table_data[0].keys()]
        # columns = [a.name for a in table_data.get_attributes()]
        pd_data = pd.DataFrame.from_records(table_data, columns=col_list)
        excell_conn = None
        if to_file:
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell

            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
        return dict({"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_conn})


if __name__ == '__main__':
    connector = ConnASQLDataGet()
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
        'to_file': True,
    }

    task1 = connector.get_col_data_from_table_date_filtered(**req_dict)
    data = loop.run_until_complete(task1)
    print(data)
    # loop.run_until_complete(connector.get_all_data_from_table('payments_in_table', to_file=True))
    # print(connector.create_connection())
    # print(connector.close_connection())

    # print(connector.get_all_tables_list())
    # print(connector.get_pd_from_table(table_name='payments_out_table', to_file=True))
    # print(connector.get_pd_from_table(table_name='pgsql_service_fields', to_file=True))
    print("finish")