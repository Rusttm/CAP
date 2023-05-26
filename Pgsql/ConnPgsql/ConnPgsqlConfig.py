# from CAPMain.CAPMainClass import CAPMainClass
from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass

# import os
# import re
# import pathlib
# import configparser


class ConnPgsqlConfig(ConnPgsqlMainClass):
    """ configfile connector"""
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
        conf = dict()
        if self.method == "file":
            conf = ConnPgsqlConfigFile().get_config_data()
        return {'url': conf.get(url, "None"),
                'port': conf.get(port, "None"),
                'user': conf.get(user, "None"),
                'user_pass': conf.get(user_pass, "None"),
                'db_name': conf.get(db_name, "None")}


if __name__ == '__main__':
    connector = ConnPgsqlConfig()
    print(connector.get_config())
