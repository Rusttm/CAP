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

    async def create_connection(self):
        print(self.__config_dict)
        try:
            # self._conn = await asyncpg.connect(user=self.__config_dict.get("user"),
            #                                    password=self.__config_dict.get("password"),
            #                                    host=self.__config_dict.get("host"),
            #                                    database=self.__config_dict.get("database"),
            #                                    port=self.__config_dict.get("port"))
            self._conn = await asyncpg.connect(**self.__config_dict)

            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new connection error: {e}")
            return False

    async def close_connection(self):

        await self._conn.close()



    async def get_all_data_from_table(self, table_name: str, to_file=False):
        _conn = await asyncpg.connect(**self.__config_dict)
        table_data = await _conn.fetch(f'SELECT * FROM {table_name}')
        await _conn.close()
        columns = [col for col in table_data[0].keys()]
        pd_data = pd.DataFrame.from_records(table_data, columns=columns)
        if to_file:
            from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
            excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=pd_data, file_name=table_name)
            print(excell_conn)
        return pd_data


    # def get_pd_from_table(self, table_name=None, to_file=False):
    #     if table_name:
    #         df = pd.read_sql(f'select * from {table_name}', con=self._engine)
    #         if to_file:
    #             from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
    #             excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=df, file_name=table_name)
    #             print(excell_conn)
    #         return df
    #     return None
    #
    # def get_all_tables_list(self):
    #     inspector = sqlalchemy.inspect(self._engine)
    #     return inspector.get_table_names()


if __name__ == '__main__':
    connector = ConnASQLDataGet()
    loop = asyncio.new_event_loop()
    # loop.run_until_complete(connector.create_connection())
    # loop.run_until_complete(connector.close_connection())
    loop.run_until_complete(connector.get_all_data_from_table('pgsql_service_fields', to_file=True))
    loop.run_until_complete(connector.get_all_data_from_table('payments_in_table', to_file=True))
    # print(connector.create_connection())
    # print(connector.close_connection())

    # print(connector.get_all_tables_list())
    # print(connector.get_pd_from_table(table_name='payments_out_table', to_file=True))
    # print(connector.get_pd_from_table(table_name='pgsql_service_fields', to_file=True))
    print("finish")