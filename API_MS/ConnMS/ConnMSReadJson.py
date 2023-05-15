from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
import json
import os
import re


class ConnMSReadJson(ConnMSMainClass):
    """read and return data from json file"""
    dir_name = "config"

    def get_config_json_data(self, file_name=None):
        """ extract data from MS json file
        return dict """
        if file_name:
            try:
                file = os.path.dirname(os.path.dirname(__file__))
                if not re.search('json', file_name):
                    file_name += '.json'
                CONF_FILE_PATH = os.path.join(file, self.dir_name, file_name)
                with open(CONF_FILE_PATH) as json_file:
                    data = json.load(json_file)
                self.logger.debug(f"{__class__.__name__} got data from json file")
                return data
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} can't read json file!", e)
                return None
        else:
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    "Please, declare existing json file name with 'file_name='")


if __name__ == '__main__':
    connector = ConnMSReadJson()
    print(connector.get_config_json_data(file_name='product_fields.json'))
