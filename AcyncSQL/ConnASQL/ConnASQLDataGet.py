from AcyncAlchemy.ConnAA.ConnAAMainClass import ConnAAMainClass
import sqlalchemy
import pandas.io.sql as pd_psql
import pandas as pd
import asyncio
import asyncpg

class ConnAADataGet(ConnAAMainClass):
    _engine = None
    __url = None

    def __init__(self):
        super().__init__()
        self.__url = self.get_url()

    def create_engine(self):
        try:
            self._engine = sqlalchemy.create_engine(self.__url, echo=True, pool_size=6, max_overflow=10)
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new engine error: {e}")
            return False

    def get_pd_from_table(self, table_name=None, to_file=False):
        if table_name:
            df = pd.read_sql(f'select * from {table_name}', con=self._engine)
            if to_file:
                from AcyncSQL.ConnASQL.ConnASQLSaveExcell import ConnASQLSaveExcell
                excell_conn = ConnASQLSaveExcell().save_pd_excell_file(data_pd=df, file_name=table_name)
                print(excell_conn)
            return df
        return None

    def get_all_tables_list(self):
        inspector = sqlalchemy.inspect(self._engine)
        return inspector.get_table_names()


if __name__ == '__main__':
    connector = ConnAADataGet()
    print(connector.create_engine())
    print(connector.get_all_tables_list())
    print(connector.get_pd_from_table(table_name='payments_out_table', to_file=True))
    # print(connector.get_pd_from_table(table_name='pgsql_service_fields', to_file=True))