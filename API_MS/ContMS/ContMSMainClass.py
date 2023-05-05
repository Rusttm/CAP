from Main.CAPMainClass import CAPMainClass
import configparser
import os

class ContMSMainClass(CAPMainClass):
    """ superclass for all MoiSklad controllers """
    id = 0

    def __init__(self):
        super().__init__()
        self.id += 1
        """ all controllers have own id"""

    def get_config_data(self):
        """ return data from config file"""
        try:
            conf = configparser.ConfigParser()
            file = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(file, "config", "config.ini")
            if not os.path.exists(CONF_FILE_PATH):
                self.logger.error(f"config file {CONF_FILE_PATH} doesnt exist")
            conf.read(CONF_FILE_PATH)
            self.logger.info(f"{__file__} got info from configfile")
            return conf
        except Exception as e:
            self.logger.error("Cant read config file", e)
            # print(e)
            return None
