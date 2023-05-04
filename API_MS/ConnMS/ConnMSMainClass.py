from Main.CAPMainClass import CAPMainClass
import requests
import json
import os
import re


class ConnMSMainClass(CAPMainClass):
    """ superclass for all MoiSklad connectors """
    id = 0
    __api_url = str()
    __api_token = str()
    __api_param_line = "?"
    __to_file = False

    def __init__(self):
        super().__init__()
        self.id += 1
        """ all connector have own id"""

    def get_conn_id(self):
        return self.id

    def set_api_config(self, api_url="", api_token="", api_param_line="", to_file=False):
        self.__api_url = api_url
        self.__api_token = api_token
        self.__api_param_line = api_param_line
        self.__to_file = to_file

    def set_api_token(self, api_token=None):
        self.__api_token = api_token

    def set_api_url(self, api_url=None):
        self.__api_url = api_url

    def set_api_param_line(self, api_param_line=None):
        if api_param_line:
            if self.__api_param_line == "?":
                self.__api_param_line += api_param_line
            elif self.__api_param_line != "?":
                self.__api_param_line = "?" + api_param_line
        else:
            self.__api_param_line = "?"
        # self.__api_param_line = api_param_line

    def add_api_param_line(self, add_param_line=None):
        if self.__api_param_line == "?":
            self.__api_param_line += add_param_line
        elif self.__api_param_line == "":
            self.__api_param_line += "?" + add_param_line
        elif self.__api_param_line != "?":
            # checking and exclude offset in request string
            x = re.split("&offset", self.__api_param_line)
            self.__api_param_line = x[0] + "&" + add_param_line
        else:
            self.__api_param_line = ""


    def get_single_req_data(self):
        """ api connect and get data in one request
        return dictionary!"""
        header_for_token_auth = {'Authorization': f'Bearer {self.__api_token}'}
        api_url = self.__api_url + self.__api_param_line
        try:
            acc_req = requests.get(url=api_url, headers=header_for_token_auth)
            # if write to file and checked to_file==True
            if self.__to_file:
                file = os.path.dirname(os.path.dirname(__file__))
                DATA_FILE_PATH = os.path.join(file, "data", f"{__name__}_req.json")
                # open(DATA_FILE_PATH, "x")
                if os.path.exists(DATA_FILE_PATH):
                    with open(DATA_FILE_PATH, 'w') as ff:
                        json.dump(acc_req.json(), ff, ensure_ascii=False)
                    self.logger.info("request was wrote to file")
                else:
                    self.logger.error(f"file {DATA_FILE_PATH} doesnt exist")
                return None
            # if data return not in file
            else:
                self.logger.info("requested successful")
                return acc_req.json()

        except IndexError:
            print('Cant read account data', Exception)
            self.logger.warning("cant connect to balance")
            return None

    def get_api_data(self):
        """ if there are more than 1000 positions
        needs to form request for getting full data"""
        offset = 1000
        data = self.get_single_req_data()
        delta = 0
        try:
            delta = int(data['meta']['size']) - int(data['meta']['offset'])
        except Exception as e:
            print(e)
        if delta > offset:
            self.logger.info(f"request from {__file__} have more than 1000rows")
            requests_num = delta//offset
            for i in range(requests_num):
                self.add_api_param_line(f"offset={(i+1)*1000}")
                next_data = self.get_single_req_data()
                for pos_num, pos in enumerate(next_data['rows']):
                    data['rows'].append(pos)
        return data

