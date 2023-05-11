# from Main.CAPMainClass import CAPMainClass
from Pgsql.ConnPgsql.ConnPgsqlConfigFile import ConnPgsqlConfigFile

import os
import re
import pathlib
import configparser


class ConnPgsqlConfig(ConnPgsqlConfigFile):
    """ configfile connector"""
    conf = None
    method = 'file'

    # url = None
    # port = None
    # user = None
    # user_pass = None
    def __init__(self):
        super().__init__()

    def get_config(self, url='url', port='port', user='user', user_pass='user_pass'):
        """ return information from config file"""
        if self.method == "file":
            self.conf = ConnPgsqlConfigFile().get_config_data()
        return {'url': self.conf[url],
                'port': self.conf[port],
                'user': self.conf[user],
                'user_pass': self.conf[user_pass]}


if __name__ == '__main__':
    connector = ConnMSConfig()
    print(connector.get_config())
