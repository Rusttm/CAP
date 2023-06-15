from API_Aiogram.ATGBotMainClass import ATGBotMainClass


import os
import re
import configparser


class ConnATGBConfig(ATGBotMainClass):
    """ configfile connector"""
    conf = None
    method = 'file'

    def __init__(self):
        super().__init__()

    def get_config(self):
        from API_Aiogram.ConnATGbot.ConnATGBConfigFile import ConnTGBConfigFile
        if self.method == "file":
            self.conf = ConnTGBConfigFile().get_config_data()
        return self.conf


if __name__ == '__main__':
    connector = ConnATGBConfig()
    print(connector.get_config()['TELEGRAMBOT'])

