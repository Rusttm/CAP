# from CAPMain.CAPMainClass import CAPMainClass
# from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
import os
import pandas as pd
import re


class ConnASQLSaveExcell(ConnASQLMainClass):
    """ connector: save dictionary data file to json """
    dir_name = "data"
    file_name = "alchemy_requested_data.xlsx"
    ext = ".xlsx"

    def save_pd_excell_file(self, data_pd: pd.DataFrame, file_name=None, dir_name=None):
        """ save dictionary data file to json
        return True or False"""
        try:
            if file_name:
                self.file_name = self.corrected_file_name(file_name)
            # if dir_name == "config":
            if dir_name:
                self.dir_name = dir_name
            dir_file = os.path.dirname(os.path.dirname(__file__))
            dir_path = os.path.join(dir_file, self.dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            DATA_FILE_PATH = os.path.join(dir_path, f"{self.file_name}")
            if not os.path.exists(DATA_FILE_PATH):
                open(DATA_FILE_PATH, 'x')
            if os.path.exists(DATA_FILE_PATH):
                data_pd.to_excel(DATA_FILE_PATH, index=False)
                self.logger.debug(f"{__class__.__name__} saved data to excell file {DATA_FILE_PATH}")
                return True
            else:
                self.logger.error(f"{__class__.__name__} can't read excell file, it doesnt exist!")
                # print(f"{__class__.__name__} can't write data to file {self.file_name}")
                return False
        except Exception as e:
            self.logger.error(f"{__class__.__name__} can't write to excell file! {e}")
            # print(e)
        # finally:
        #     return False


    def corrected_file_name(self, file_name):
        """ return corrected file name in filename.json"""
        if re.search(self.ext, file_name):
            return file_name
        else:
            return f"{file_name}{self.ext}"








if __name__ == '__main__':
    connector = ConnASQLSaveExcell()
    # print(connector.save_data_json_file(data_dict={"data": "some data"}, file_name="temporary_file"))
