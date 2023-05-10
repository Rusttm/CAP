# from Main.CAPMainClass import CAPMainClass
import os
import json
import re


class ConnMSSaveFile(object):
    """ connector: save dictionary data file to json """
    dir_name = "data"
    file_name = "ms_requested_data.json"

    def save_data_json_file(self, data_dict=None, file_name=None):
        """ save dictionary data file to json
        return True or False"""
        try:
            if file_name:
                self.file_name = self.corrected_file_name(file_name)
            up_up_dir_file = os.path.dirname(os.path.dirname(__file__))
            DATA_FILE_PATH = os.path.join(up_up_dir_file, self.dir_name, f"{self.file_name}")
            if not os.path.exists(DATA_FILE_PATH):
                open(DATA_FILE_PATH, 'x')
            if os.path.exists(DATA_FILE_PATH) and data_dict:
                with open(DATA_FILE_PATH, 'w') as ff:
                    json.dump(data_dict, ff, ensure_ascii=False)
                return True
            else:
                print(f"{__class__.__name__} can't write data to file {self.file_name}")
                return False
        except Exception as e:
            print(e)
            return False

    def corrected_file_name(self, file_name):
        """ return corrected file name in filename.json"""
        if re.search("json", file_name):
            return file_name
        else:
            return f"{file_name}.json"








if __name__ == '__main__':
    connector = ConnMSSaveFile()
    print(connector.save_data_json_file({"data": "some data"}))
