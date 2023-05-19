from API_Tbot.ConnTbot.ConnTGBotMainClass import ConnTGBotMainClass


import os
import re

import configparser


class ConnTGBConfig(ConnTGBotMainClass):
    """ configfile connector"""
    conf = None
    method = 'file'

    def __init__(self):
        super().__init__()

    def get_config(self):
        from API_Tbot.ConnTbot.ConnTGBConfigFile import ConnTGBConfigFile
        if self.method == "file":
            self.conf = ConnTGBConfigFile().get_config_data()
        return self.conf


if __name__ == '__main__':
    connector = ConnTGBConfig()
    print(connector.get_config()['TELEGRAMBOT'])

