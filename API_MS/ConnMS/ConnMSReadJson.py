# from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
import json
import os
import re
class ConnMSReadJson(object):
    """read and return data from json file"""
    dir_name = "config"

    def get_config_json_data(self, file_name=None):
        """ extract data from MS json file
        return dict """
        if file_name:
            try:
                # data = None
                file = os.path.dirname(os.path.dirname(__file__))
                if not re.search('json', file_name):
                    file_name += '.json'
                CONF_FILE_PATH = os.path.join(file, self.dir_name, file_name)
                with open(CONF_FILE_PATH) as json_file:
                    data = json.load(json_file)
                return data
            except Exception as e:
                print(e)
                return None
        else:
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    "Please, declare existing json file name with 'file_name='")


if __name__ == '__main__':
    connector = ConnMSReadJson()
    print(connector.get_config_json_data(file_name='product_fields.json'))