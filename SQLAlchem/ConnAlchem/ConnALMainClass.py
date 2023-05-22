# from https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh

from SQLAlchem.SQLAlchemMainClass import SQLAlchemMainClass
import sqlalchemy
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class ConnALMainClass(SQLAlchemMainClass):

    def __init__(self, name=None):
        super().__init__()
        self.engine = None

    def create_engine(self):
        from SQLAlchem.ConnAlchem.ConnALConfig import ConnALConfig
        try:
            conf = dict(ConnALConfig().get_config())
            host = conf.get('url', '')
            port = conf.get('port', '')
            database = conf.get('db_name', '')
            user = conf.get('user', '')
            password = conf.get('user_pass', '')
            self.logger.debug(f"{__class__.__name__} read data from config")
            self.engine = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host},{port}/{database}",
                                                   echo=True, pool_size=6, max_overflow=10)
            self.engine.connect()
            # self.metadata = sqlalchemy.MetaData()
            # print(self.engine)
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector in SQLAlchemy! {e}")

    def create_database_pgsql(self, db_name=None):
        """ doesnt work now"""
        if db_name:
            from SQLAlchem.ConnAlchem.ConnALConfig import ConnALConfig
            try:
                conf = dict(ConnALConfig().get_config())
                host = conf.get('url', '')
                port = conf.get('port', '')
                user = conf.get('user', '')
                password = conf.get('user_pass', '')
                self.logger.debug(f"{__class__.__name__} read data from config")
                connection = psycopg2.connect(host=host, port=port, user=user, password=password, )
                connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = connection.cursor()
                cursor.execute(f"create database {db_name}")
                cursor.close()
                connection.close()
            except Exception as e:
                print(f"configuration data not loaded {e}")
                self.logger.error(f"{__class__.__name__} can't create connector in psycopg2! {e}")

    def create_empty_table(self, table_name=None):
        try:
            self.last_metadata = sqlalchemy.MetaData()
            # new_table = sqlalchemy.Table(name=table_name, metadata=self.last_metadata, autoload_replace=True, autoload_with=self.engine)
            new_table = sqlalchemy.Table(table_name, self.last_metadata)
            print(repr(self.last_metadata.tables))
            print(repr(self.last_metadata.tables[table_name]))
            print(new_table.columns.keys())
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new empty table error: {e}")
            return False


if __name__ == '__main__':
    connector = ConnALMainClass()
    connector.create_engine()
    print(sqlalchemy.__version__)
    # connector.create_database_pgsql(db_name="testdb")
    connector.create_empty_table(table_name="TestTable")

