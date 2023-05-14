from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
from API_MS.ConnMS.ConnMSSaveFile import ConnMSSaveFile
import os
import pandas as pd
# import openpyxl


class ConnMSExcell(ConnMSMainClass, ConnMSSaveFile):
    """ api fields convertor from excell to json:
    {"type":"product", "data":{"id":{"type":"UUID", "filters":"=,!=", "descr":"ID товара"}}} """
    dir_name = "data"
    file_name = None

    def __init__(self):
        super().__init__()

    def get_excell_data(self):
        """ extract data from excell file
        return dictionary """
        result = dict({"type": "product", "data": {}})
        if self.file_name:
            try:
                if self.dir_name == "config":
                    file = os.path.dirname(__file__)
                elif self.dir_name == "data":
                    file = os.path.dirname(os.path.dirname(__file__))
                else:
                    file = __file__
                CONF_FILE_PATH = os.path.join(file, self.dir_name, self.file_name)
                file_data = pd.read_excel(CONF_FILE_PATH, index_col=0)
                file_data = file_data.where(pd.notnull, None)
                file_data = file_data.replace(r'\n', ' ', regex=True)
                file_data.columns = ["type", "filters", "descr"]
                test_dict = file_data.to_dict('index')
                result['data'] = test_dict
                self.save_data_json_file(data_dict=result, file_name='product_fields')
                return result
            except Exception as e:
                print(e)
                return None
        else:
            return None

    def set_excell_file(self, file_name=None):
        """ sets file name"""
        if file_name:
            self.file_name = file_name


if __name__ == '__main__':
    connector = ConnMSExcell()
    connector.set_excell_file(file_name='prod_fields.xlsx')
    print(connector.get_excell_data())
