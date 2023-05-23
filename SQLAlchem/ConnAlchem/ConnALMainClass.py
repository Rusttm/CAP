# from https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh

from SQLAlchem.SQLAlchemMainClass import SQLAlchemMainClass
import sqlalchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class ConnALMainClass(SQLAlchemMainClass):

    def __init__(self, name=None):
        super().__init__()
        self.engine = None

    def types_mapper(self, type=None):
        mapper = dict({
            "String(255)": postgresql.INET,
            "Boolean": postgresql.BOOLEAN,
            "UUID": postgresql.UUID,
            "Array(Object)": postgresql.ARRAY,
            "Object": postgresql.JSON,
            "Meta": postgresql.JSON,
            "String(4096)": postgresql.TEXT,
            "Int": postgresql.INTEGER,
            "MetaArray": postgresql.ARRAY,
            "String": postgresql.TEXT,
            "Enum": postgresql.TEXT,
            "DateTime": postgresql.DATE
        })
        return mapper.get(type, postgresql.TEXT)

    def create_url(self):
        from SQLAlchem.ConnAlchem.ConnALConfig import ConnALConfig
        try:
            conf = dict(ConnALConfig().get_config())
            host = conf.get('url', '')
            port = conf.get('port', '')
            database = conf.get('db_name', '')
            user = conf.get('user', '')
            password = conf.get('user_pass', '')
            self.logger.debug(f"{__class__.__name__} read data from config")
            self.url = f"postgresql://{user}:{password}@{host},{port}/{database}"
            self.url_temp = f"postgresql://{user}:{password}@{host},{port}/"
             # self.cur = self.conn.cursor()
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

    def delete_database_alchemy(self, db_name=None):
        if database_exists(self.url_temp+db_name):
            drop_database(self.url_temp+db_name)
        else:
            # Connect the database if exists.
            self.engine.connect()
    def create_database_alchemy(self, db_name=None):
        if not database_exists(self.url_temp+db_name):
            create_database(self.url_temp+db_name)
        else:
            # Connect the database if exists.
            self.engine.connect()


    def create_empty_table(self, table_name=None):
        try:
            self.engine = sqlalchemy.create_engine(self.url, echo=True, pool_size=6, max_overflow=10)
            self.last_metadata = sqlalchemy.MetaData()
            # new_table = sqlalchemy.Table(name=table_name, metadata=self.last_metadata, autoload_replace=True, autoload_with=self.engine)
            # new_table = sqlalchemy.Table(table_name, self.last_metadata, Column("id", Integer, primary_key=True))
            sqlalchemy.Table(table_name, self.last_metadata)
            # print(repr(self.last_metadata.tables))
            # print(repr(self.last_metadata.tables[table_name]))
            # print(new_table.columns.keys())
            # new_table.create(self.engine)
            self.last_metadata.create_all(self.engine)
            # self.engine.connect()
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new empty table error: {e}")
            return False

    def add_column_2table(self, table_name=None, column_dict=None):
        """  column_dict {"name":"info", "type":"String(255)", "primary_key":False, "default":"None"}"""
        column_name = column_dict.get("name", "None")
        column_type = column_dict.get("type", "None")
        # self.conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
        primary = column_dict.get("primary_key", False)
        default_value = column_dict.get("default", None)
        alchemy_type = self.types_mapper(column_type)
        col = sqlalchemy.Column(column_name, alchemy_type, primary_key=primary, default=default_value)
        col_name = col.compile(dialect=self.engine.dialect)
        col_type = col.type.compile(self.engine.dialect)

        self.conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}")
        print(repr(self.last_metadata.tables))
        self.engine.connect()

if __name__ == '__main__':
    connector = ConnALMainClass()
    connector.create_url()
    print(sqlalchemy.__version__)
    # connector.create_database_alchemy(db_name="newdb")
    # connector.delete_database_alchemy(db_name="newdb")
    table_name = "TestTable"
    # connector.create_database_pgsql(db_name="testdb")
    connector.create_empty_table(table_name=table_name)
    table_name = "TestEmpty3Table"
    connector.create_empty_table(table_name=table_name)
    # column_dict = {"name": "info", "type": "String(255)", "primary_key": False, "default": "None"}
    # connector.add_column_2table(table_name=table_name, column_dict=column_dict)

