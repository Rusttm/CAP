# from CAPMain.CAPMainClass import CAPMainClass
from Pgsql.ConnPgsql.ConnPgsqlConfig import ConnPgsqlConfig
import os
import configparser


class ConnPgsqlConfigFile(ConnPgsqlConfig):
    """ configfile connector"""
    dir_name = "config"
    file_name = "sqlconfig.ini"


    def get_config_data(self, sector='POSTGRESQL'):
        """ extract data from sql config file
        return config section POSTGRESQL """
        try:
            conf = configparser.ConfigParser()
            # sections_list = conf.sections()
            configuration = None
            up_up_dir = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(up_up_dir, self.dir_name, self.file_name)
            conf.read(CONF_FILE_PATH)
            if sector in conf.sections():
                configuration = conf[sector]
            self.logger.debug(f"module {__class__.__name__} read configfile")
            return configuration
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't read config file", e)
            return None

    def get_full_config_data(self):
        """ extract data from sql config file
        return config section POSTGRESQL """
        try:
            conf = configparser.ConfigParser()
            # sections_list = conf.sections()
            configuration = None
            up_up_dir = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(up_up_dir, self.dir_name, self.file_name)
            conf.read(CONF_FILE_PATH)
            configuration = conf
            self.logger.debug(f"module {__class__.__name__} read configfile")
            return configuration
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't read config file", e)
            return None

if __name__ == '__main__':
    connector = ConnPgsqlConfigFile()
    print(connector.get_full_config_data())
    print(connector.get_config_data())