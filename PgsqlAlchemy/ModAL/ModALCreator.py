from PgsqlAlchemy.ModAL.ModALMainClass import ModALMainClass
from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
import sqlalchemy
class ModALCreator(ConnALMainClass, ModALMainClass):
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


if __name__ == '__main__':
    connector = ModALCreator()
    print(f"logger file name: {connector.logger_name}")