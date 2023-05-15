# from Main.CAPMainClass import CAPMainClass
from API_MS.ConnMS.ConnMSConfig import ConnMSConfig
import os
import configparser
import pathlib

class ConnMSConfigFile(ConnMSConfig):
    """ configfile connector"""
    dir_name = "config"
    file_name = "msconfig.ini"


    def get_config_data(self, sector='MoiSklad'):
        """ extract data from MoiSklad config file
        return config section MoiSklad """
        try:
            conf = configparser.ConfigParser()
            file = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(file, self.dir_name, self.file_name)
            conf.read(CONF_FILE_PATH)
            self.logger.debug(f"{pathlib.PurePath(__file__).name} got info from configfile")
            return conf[sector]
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't read msconfig file", e)
            print(e)
            return None


if __name__ == '__main__':
    connector = ConnMSConfigFile()
    print(connector.get_config_data())