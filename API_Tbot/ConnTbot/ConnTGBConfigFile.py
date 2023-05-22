# from CAPMain.CAPMainClass import CAPMainClass
from API_Tbot.ConnTbot.ConnTGBConfig import ConnTGBConfig
import os
import configparser
import pathlib

class ConnTGBConfigFile(ConnTGBConfig):
    """ configfile connector"""
    dir_name = "config"
    file_name = "tgbconfig.ini"


    def get_config_data(self, sector='TELEGRAMBOT'):
        """ extract data from TELEGRAMBOT config file
        return config section TELEGRAMBOT """
        try:
            conf = configparser.ConfigParser()
            file = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(file, self.dir_name, self.file_name)
            conf.read(CONF_FILE_PATH)
            self.logger.debug(f"{pathlib.PurePath(__file__).name} got info from configfile")
            return conf
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't read msconfig file", e)
            # print(e)
            return None


if __name__ == '__main__':
    connector = ConnTGBConfigFile()
    print(connector.get_config_data())