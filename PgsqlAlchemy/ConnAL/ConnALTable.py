from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
import sqlalchemy


class ConnALTable(ConnALMainClass):
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

    def get_all_tables_list(self):
        self.create_engine()
        inspector = sqlalchemy.inspect(self._engine)
        return inspector.get_table_names()

    def check_table_exist(self, table_name: str = None):
        self.create_engine()
        # res = self._engine.dialect.has_table(self._engine.connect(), table_name=table_name, schema='dbo')
        res = self._engine.dialect.has_table(connection=self._engine.connect(), table_name=table_name)

        return res


if __name__ == '__main__':
    connector = ConnALTable()
    # print(connector.create_engine())
    # print(connector.get_all_tables_list())
    print(connector.check_table_exist("invin_model"))