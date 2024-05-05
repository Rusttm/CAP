from Parser.ParserMainClass import ParserMainClass


class ConnParserConfig(ParserMainClass):
    """ configfile connector"""
    _conf = None
    dir_name = "config"
    file_name = "parser_conf.json"

    def __init__(self):
        super().__init__()

    def load_config(self):
        """ return information from config file"""
        from Parser.ConnParser.ConnParserJson import ConnParserJson
        self._conf = ConnParserJson().get_data_from_json(file_name=self.file_name, dir_name=self.dir_name)
        return self._conf


if __name__ == '__main__':
    connector = ConnParserConfig()
    print(connector.load_config())
