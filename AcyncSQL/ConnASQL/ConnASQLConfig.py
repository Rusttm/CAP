from AcyncSQL.ASQLMainClass import ASQLMainClass


class ConnASQLConfig(ASQLMainClass):
    """ configfile connector"""
    conf = None
    method = 'file'

    # url = None
    # port = None
    # user = None
    # user_pass = None
    def __init__(self):
        super().__init__()

    def get_config(self, url='url', port='port', user='user', user_pass='user_pass', db_name='db_name'):
        """ return information from config file"""
        from AcyncAlchemy.ConnAA.ConnAAConfigFile import ConnAAConfigFile
        if self.method == "file":
            self.conf = ConnAAConfigFile().get_config_data()
        return {'url': self.conf[url],
                'port': self.conf[port],
                'user': self.conf[user],
                'user_pass': self.conf[user_pass],
                'db_name': self.conf[db_name]}


if __name__ == '__main__':
    connector = ConnASQLConfig()
    print(connector.get_config())
