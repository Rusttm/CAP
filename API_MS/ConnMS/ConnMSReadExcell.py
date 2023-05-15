from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
# from API_MS.ConnMS.ConnMSSaveFile import ConnMSSaveFile
import os
import pandas as pd
# import openpyxl
import re

class ConnMSReadExcell(ConnMSMainClass):
    """ read api fields convertor from excell and return json:
    {"type":"product", "data":{"id":{"type":"UUID", "filters":"=,!=", "descr":"ID товара"}}} """
    dir_name = "data"
    names_dict = {"Название": "name", "Тип": "type", "Фильтрация": "filter", "Описание": "descr"}
    table_columns = []
    def __init__(self):
        super().__init__()

    def get_excell_data(self, file_name=None):
        """ extract data from excell file
        return dictionary """
        result = dict({"table": file_name.split('.')[0], "data": {}})
        if file_name:
            self.table_columns = []
            if not re.search('xlsx', file_name):
                file_name += '.xlsx'
            try:
                # choose directory to read data
                if self.dir_name == "config":
                    file = os.path.dirname(__file__)
                elif self.dir_name == "data":
                    file = os.path.dirname(os.path.dirname(__file__))
                else:
                    file = __file__
                CONF_FILE_PATH = os.path.join(file, self.dir_name, file_name)
                file_data = pd.read_excel(CONF_FILE_PATH, index_col=0, header=None)
                file_data = file_data.where(pd.notnull, None)
                file_data = file_data.replace(r'\n', ' ', regex=True)
                # some tables copied with wrong hat
                row_index = 1
                while row_index < file_data.shape[0]-1:
                    # print(file_data.iloc[0, :])
                    if file_data.iloc[0, 0] == "Тип":
                        for col in range(file_data.shape[1]):
                            # print()
                            col_name = file_data.iloc[0, col]
                            self.table_columns.append(self.names_dict[col_name])
                        file_data = file_data.drop(file_data.index[0])
                        break
                    else:
                        file_data = file_data.drop(file_data.index[0])
                        # file_data.drop(labels=0, axis=0)
                        row_index += 1
                if row_index == file_data.shape[0]-2:
                    print(f"Excell file {CONF_FILE_PATH} not contain necessary data")
                # file_data.columns = ["type", "filters", "descr"]
                file_data.columns = self.table_columns
                test_dict = file_data.to_dict('index')
                result['data'] = test_dict
                self.logger.debug(f"{__class__.__name__} got data from excell file")
                return result
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} can't read excell file {e}")
                return None
        else:
            import errno
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "Please declare existing excell file name")


if __name__ == '__main__':
    connector = ConnMSReadExcell()
    print(connector.get_excell_data(file_name='invin_fields.xlsx'))
