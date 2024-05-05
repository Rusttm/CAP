from Parser.ParserMainClass import ParserMainClass


class ConnParserConfig(ParserMainClass):
    """ configfile connector"""
    conf = None
    dir_name = "config"
    file_name = "parser_conf.json"

    def __init__(self):
        super().__init__()

    def get_config(self):
        """ return information from config file"""
        from Parser.ConnParser.ConnParserJson import ConnParserJson
        self.conf = ConnParserJson().get_data_from_json(file_name=self.file_name, dir_name=self.dir_name)
        return {"user_agents": self.conf.get("user_agents")}


if __name__ == '__main__':
    connector = ConnParserConfig()
    print(connector.get_config())
