# from https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh
from AcyncSQL.ASQLMainClass import ASQLMainClass


class ConnASQLMainClass(ASQLMainClass):
    """ main class only create url string"""
    # __url_no_db = None
    __config_dict = dict()
    def __init__(self, name=None):
        super().__init__()

    def get_conn_dict(self) -> dict:
        from AcyncSQL.ConnASQL.ConnASQLConfig import ConnASQLConfig
        try:
            self.__config_dict = dict(ConnASQLConfig().get_config())
            self.logger.debug(f"{__class__.__name__} read data from config")
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector in SQLAlchemy! {e}")
        return self.__config_dict


if __name__ == '__main__':
    connector = ConnASQLMainClass()
    print(connector.get_conn_dict())
