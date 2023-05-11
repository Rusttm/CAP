# from Main.CAPMainClass import CAPMainClass
import os
import configparser


class ConnPgsqlConfigFile(object):
    """ configfile connector"""
    dir_name = "config"
    file_name = "sqlconfig.ini"


    def get_config_data(self, sector='POSTGRESQL'):
        """ extract data from sql config file
        return config section POSTGRESQL """
        try:
            conf = configparser.ConfigParser()
            up_up_dir = os.path.dirname(os.path.dirname(__file__))
            CONF_FILE_PATH = os.path.join(up_up_dir, self.dir_name, self.file_name)
            conf.read(CONF_FILE_PATH)
            return conf[sector]
        except Exception as e:
            return None


if __name__ == '__main__':
    connector = ConnPgsqlConfigFile()
    print(connector.get_config_data())