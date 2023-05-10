from Main.CAPMainClass import CAPMainClass
from API_MS.ConnMS.ConnMSConfig import ConnMSConfig
import requests
import json
import os
import re
import pathlib


class ConnMSMainClass(CAPMainClass, ConnMSConfig):
    """ superclass for all MoiSklad connectors """
    id = 0
    __api_url = str()
    __api_token = str()
    __api_param_line = "?"
    __to_file = False
    __config = None

    def __init__(self):
        super().__init__()
        self.id += 1
        self.__config
        """ all connector have own id"""

    def get_conn_id(self):
        """ return connectors id"""
        return self.id

    def set_config(self):
        """it sets url and token in configuration"""
        try:
            conf_connector = ConnMSConfig()
            configuration = conf_connector.get_config()
            self.set_api_url(configuration['url'])
            self.set_api_token(configuration['token'])

        except Exception as e:
            self.logger.error("Cant read configuration!", e)

        # try:
        #     conf = None
        #     try:
        #         conf = self.get_config_data()
        #     except Exception as e:
        #         self.logger.error("Cant read configuration!", e)
        #     if conf:
        #         self.set_api_url(conf['MoiSklad']['url_money'])
        #         self.set_api_token(conf['MoiSklad']['access_token'])
        #     else:
        #         # self.logger.warning("cant get info from configfile url_balance or access_token")
        #         self.logger.critical("Please redefine method set_config in child class!!!")
        #     self.set_api_config()
        # except Exception as e:
        #     # self.logger.warning("cant get info from configfile url_balance or access_token")
        #     self.logger.critical("Please redefine method set_config in child class!!!")

    def set_api_config(self, api_url=None, api_token=None, api_param_line=None, to_file=False):
        self.__api_url = api_url
        self.__api_token = api_token
        self.__api_param_line = api_param_line
        self.__to_file = to_file

    def set_api_token(self, api_token=None):
        self.__api_token = api_token

    def set_api_url(self, api_url=None):
        self.__api_url = api_url

    def set_api_param_line(self, api_param_line=None):
        """ set new request parameters in url line """
        if api_param_line:
            if self.__api_param_line == "?":
                self.__api_param_line += api_param_line
            elif self.__api_param_line != "?":
                self.__api_param_line = "?" + api_param_line
        else:
            self.__api_param_line = "?"
        # self.__api_param_line = api_param_line

    def add_api_param_line(self, add_param_line=None):
        """ add request parameters in current url line"""
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
            self.logger.info(f"{pathlib.PurePath(__file__).name} make request")
            acc_req = requests.get(url=api_url, headers=header_for_token_auth)
            try:
                # check errors in request
                errors_request = acc_req.json()['errors']
                for error in errors_request:
                    self.logger.error(
                        f"{pathlib.PurePath(__file__).name} requested information has errors: {error['error']} (code {error['code']}) ")
            except Exception as e:
                self.logger.info(f"{pathlib.PurePath(__file__).name} request successful - data has context ")
            return acc_req.json()
        except Exception as e:
            # print('Cant read account data', Exception)
            self.logger.critical(f"cant connect to request data: {e}")
            return None

    def get_api_data(self, to_file=False):
        """ if there are more than 1000 positions
        needs to form request for getting full data"""
        self.__to_file = to_file
        offset = 1000
        # starts first request
        data = self.get_single_req_data()
        delta = 0
        try:
            # check full lenth of data by data['meta']['size']
            delta = int(data['meta']['size']) - int(data['meta']['offset'])
        except Exception as e:
            # if there is no data in data['meta']['size']
            self.logger.warning(f"cant find key {e} for data['meta']['size'] ")
        # if there is more than 1000 positions in row ..
        if delta > offset:
            self.logger.info(f"{pathlib.PurePath(__file__).name} request contains more than 1000rows")
            requests_num = delta // offset
            for i in range(requests_num):
                # .. request data until it ends
                self.add_api_param_line(f"offset={(i + 1) * 1000}")
                next_data = self.get_single_req_data()
                data['rows'] += next_data['rows']
                # for pos_num, pos in enumerate(next_data['rows']):
                #     data['rows'].append(pos)
        if self.__to_file:
            file = os.path.dirname(os.path.dirname(__file__))
            DATA_FILE_PATH = os.path.join(file, "data", "requested_data.json")
            if not os.path.exists(DATA_FILE_PATH):
                open(DATA_FILE_PATH, 'x')
            if os.path.exists(DATA_FILE_PATH):
                self.logger.debug(f"start write request to file {pathlib.PurePath(DATA_FILE_PATH).name}")
                with open(DATA_FILE_PATH, 'w') as ff:
                    json.dump(data, ff, ensure_ascii=False)
                self.logger.debug(f"request was wrote to file {pathlib.PurePath(DATA_FILE_PATH).name}")
            else:
                self.logger.error(f"file {DATA_FILE_PATH} doesnt exist")
        return data
