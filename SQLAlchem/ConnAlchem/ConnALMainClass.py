from SQLAlchem.SQLAlchemMainClass import SQLAlchemMainClass
import sqlalchemy


class ConnALMainClass(SQLAlchemMainClass):

    def __init__(self, name=None):
        super().__init__()
        self.engine = None

    def create_engine(self):
        from SQLAlchem.ConnAlchem.ConnALConfig import ConnALConfig
        try:
            conf = ConnALConfig().get_config()
            host = conf['url'],
            port = conf['port'],
            database = conf['db_name'],
            user = conf['user'],
            password = conf['user_pass']
            self.logger.debug(f"{__class__.__name__} read data from config")
            self.engine = sqlalchemy.create_engine(f"postgresql-psycopg2://{user}:{password}@{host},{port}/{database}")
            self.engine.connect()
            print(self.engine)
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector in SQLAlchemy! {e}")


if __name__ == '__main__':
    connector = ConnALMainClass()
    connector.create_engine()
    print(sqlalchemy.__version__)
