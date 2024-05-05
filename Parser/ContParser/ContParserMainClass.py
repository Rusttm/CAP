# from https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh
from Parser.ParserMainClass import ParserMainClass


class ContParserMainClass(ParserMainClass):
    """ main class only create url string"""
    def __init__(self):
        super().__init__()

    def get_config(self):
        _conf = None
        from Parser.ConnParser.ConnParserConfig import ConnParserConfig
        try:
            _conf = dict(ConnParserConfig().load_config())
            self.logger.debug(f"{__class__.__name__} read data from config")
        except Exception as e:
            print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't load parsing data! {e}")
        return _conf

if __name__ == '__main__':
    connector = ContParserMainClass()
    print(connector.get_config())
