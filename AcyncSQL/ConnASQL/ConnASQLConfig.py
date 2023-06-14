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

    def get_config(self, host='host', port='port', user='user', password='password', database='database'):
        """ return information from config file"""
        from AcyncSQL.ConnASQL.ConnASQLConfigFile import ConnASQLConfigFile
        if self.method == "file":
            self.conf = ConnASQLConfigFile().get_config_data()
        return {'host': self.conf[host],
                'port': self.conf[port],
                'user': self.conf[user],
                'password': self.conf[password],
                'database': self.conf[database]}


if __name__ == '__main__':
    connector = ConnASQLConfig()
    print(connector.get_config())
