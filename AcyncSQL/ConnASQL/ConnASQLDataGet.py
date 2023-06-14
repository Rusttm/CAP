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


if __name__ == '__main__':
    connector = ConnASQLDataGet()
    loop = asyncio.new_event_loop()
    # loop.run_until_complete(connector.test_connection())
    loop.run_until_complete(connector.get_all_data_from_table_with_path('pgsql_service_fields', to_file=True))
    # loop.run_until_complete(connector.get_all_data_from_table('payments_in_table', to_file=True))
    # print(connector.create_connection())
    # print(connector.close_connection())

    # print(connector.get_all_tables_list())
    # print(connector.get_pd_from_table(table_name='payments_out_table', to_file=True))
    # print(connector.get_pd_from_table(table_name='pgsql_service_fields', to_file=True))
    print("finish")