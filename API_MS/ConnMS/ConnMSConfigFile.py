# from Main.CAPMainClass import CAPMainClass
import os
import re
import pathlib
import configparser


class ConnMSConfigFile(object):
    """ configfile connector"""

    def get_config_data(self):
        """ extract data from MoiSklad config file
        return config MoiSklad section"""
        try:
            conf = configparser.ConfigParser()
            file = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(file, "config", "msconfig.ini")
            # if not os.path.exists(CONF_FILE_PATH):
                # self.logger.error(f"config file {CONF_FILE_PATH} doesnt exist")
            conf.read(CONF_FILE_PATH)
            # self.logger.info(f"{pathlib.PurePath(__file__).name} got info from configfile")
            return conf['MoiSklad']
        except Exception as e:
            # self.logger.error("Cant read config file", e)
            return None


if __name__ == '__main__':
    connector = ConnMSConfigFile()
    print(connector.get_config_data())