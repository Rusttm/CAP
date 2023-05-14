from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
from API_MS.ConnMS.ConnMSSaveFile import ConnMSSaveFile
import os
import pandas as pd
# import openpyxl
import re

class ConnMSReadExcell(object):
    """ read api fields convertor from excell and return json:
    {"type":"product", "data":{"id":{"type":"UUID", "filters":"=,!=", "descr":"ID товара"}}} """
    dir_name = "data"

    def __init__(self):
        super().__init__()

    def get_excell_data(self, file_name=None):
        """ extract data from excell file
        return dictionary """
        result = dict({"type": "product", "data": {}})
        if file_name:
            if not re.search('xlsx', file_name):
                file_name += '.xlsx'
            try:
                if self.dir_name == "config":
                    file = os.path.dirname(__file__)
                elif self.dir_name == "data":
                    file = os.path.dirname(os.path.dirname(__file__))
                else:
                    file = __file__
                CONF_FILE_PATH = os.path.join(file, self.dir_name, file_name)
                file_data = pd.read_excel(CONF_FILE_PATH, index_col=0)
                file_data = file_data.where(pd.notnull, None)
                file_data = file_data.replace(r'\n', ' ', regex=True)
                file_data.columns = ["type", "filters", "descr"]
                test_dict = file_data.to_dict('index')
                result['data'] = test_dict
                return result
            except Exception as e:
                print(e)
                return None
        else:
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Please declare existing excell file name")



if __name__ == '__main__':
    connector = ConnMSReadExcell()
    print(connector.get_excell_data(file_name='prod_fields.xlsx'))
