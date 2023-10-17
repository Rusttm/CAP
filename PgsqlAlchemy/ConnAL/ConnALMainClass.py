# from https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh
from PgsqlAlchemy.PgsqlAlchemyMainClass import PgsqlAlchemyMainClass


class ConnALMainClass(PgsqlAlchemyMainClass):
    """ main class only create url string"""
    # __url_no_db = None
    __url = None
    def __init__(self, name=None):
        super().__init__()

    def get_url(self):
        from PgsqlAlchemy.ConnAL.ConnALConfig import ConnALConfig
        try:
            conf = dict(ConnALConfig().get_config())
            host = conf.get('url', '')
            port = conf.get('port', '')
            database = conf.get('db_name', '')
            user = conf.get('user', '')
            password = conf.get('user_pass', '')
            self.logger.debug(f"{__class__.__name__} read data from config")
            self.__url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
            # self.__url_no_db = f"postgresql://{user}:{password}@{host},{port}/"
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector in SQLAlchemy! {e}")
        return self.__url


if __name__ == '__main__':
    connector = ConnALMainClass()
    print(connector.get_url())
