from PgsqlAlchemy.ConnMS.ConnMSMainClass import ConnMSMainClass


import os
import re

import configparser


class ConnMSConfig(ConnMSMainClass):
    """ configfile connector"""
    conf = None
    method = 'file'
    def __init__(self):
        super().__init__()

    def get_config(self, url_conf_key='url_money', token_conf_key='access_token'):
        from PgsqlAlchemy.ConnMS.ConnMSConfigFile import ConnMSConfigFile
        if self.method == "file":
            self.conf = ConnMSConfigFile().get_config_data()
        return {'url': self.conf[url_conf_key], 'token': self.conf[token_conf_key]}


if __name__ == '__main__':
    connector = ConnMSConfig()
    print(connector.get_config())
