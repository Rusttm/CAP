# from CAPMain.CAPMainClass import CAPMainClass
from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass

# import os
# import re
# import pathlib
# import configparser


class ConnPgsqlConfig(ConnPgsqlMainClass):
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
        from Pgsql.ConnPgsql.ConnPgsqlConfigFile import ConnPgsqlConfigFile
        if self.method == "file":

            self.conf = ConnPgsqlConfigFile().get_config_data()
        return {'url': self.conf[url],
                'port': self.conf[port],
                'user': self.conf[user],
                'user_pass': self.conf[user_pass],
                'db_name': self.conf[db_name]}


if __name__ == '__main__':
    connector = ConnPgsqlConfig()
    print(connector.get_config())
