from SQLAlchem.SQLAlchemMainClass import SQLAlchemMainClass
import sqlalchemy
import psycopg2


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
            self.engine = sqlalchemy.create_engine(f"postgresql://{user}:{password}@{host},{port}/{database}")
            self.engine.connect()
            print(self.engine)
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector in SQLAlchemy! {e}")


if __name__ == '__main__':
    connector = ConnALMainClass()
    connector.create_engine()
    print(sqlalchemy.__version__)
