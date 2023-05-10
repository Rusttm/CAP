# from Main.CAPMainClass import CAPMainClass
from API_MS.ConnMS.ConnMSConfigFile import ConnMSConfigFile

import os
import re
import pathlib
import configparser


class ConnMSConfig(ConnMSConfigFile):
    """ configfile connector"""
    conf = None
    method = 'file'
    def __init__(self):
        super().__init__()

    def get_config_data(self):
        """ extract data from config file
        return keys and values """
        try:
            conf = configparser.ConfigParser()
            file = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(file, "config", "msconfig.ini")
            if not os.path.exists(CONF_FILE_PATH):
                self.logger.error(f"config file {CONF_FILE_PATH} doesnt exist")
            conf.read(CONF_FILE_PATH)
            self.logger.info(f"{pathlib.PurePath(__file__).name} got info from configfile")
            return conf
        except Exception as e:
            self.logger.error("Cant read config file", e)
            return None

    def get_config(self, url_conf_key='url_money', token_conf_key='access_token'):
        if self.method == "file":
            self.conf = ConnMSConfigFile().get_config_data()
        return {'url': self.conf[url_conf_key], 'token': self.conf[token_conf_key]}


if __name__ == '__main__':
    connector = ConnMSConfig()
    print(connector.get_config())
