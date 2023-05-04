import json
from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
import requests
import logging
import os


# import sys
class ConnMSBalance(ConnMSMainClass):
    """ connector to MoiSklad balance """
    accounts = dict()
    __api_url = ""
    __api_token = ""
    __to_file = False

    def __init__(self):
        super().__init__()

    def set_api_config(self, api_url, api_token, to_file=False):
        self.__api_url = api_url
        self.__api_token = api_token
        self.__to_file = to_file
    def get_api_data(self):
        """ api connect and get data"""
        header_for_token_auth = {'Authorization': f'Bearer {self.__api_token}'}
        try:
            acc_req = requests.get(url=self.__api_url, headers=header_for_token_auth)
            # if checked to_file==True
            if self.__to_file:
                DATA_FILE_PATH = os.path.join(os.path.dirname(os.getcwd()), "data", "balance_req_list.json")
                if os.path.exists(DATA_FILE_PATH):
                    with open(DATA_FILE_PATH, 'w') as ff:
                        json.dump(acc_req.json(), ff, ensure_ascii=False)
                    self.logger.info("request was wrote to file")
                else:
                    self.logger.error(f"file {DATA_FILE_PATH} doesnt exist")
                return None
            # if data return not in file
            else:
                return acc_req.json()

        except IndexError:
            print('Cant read account data', Exception)
            logging.warning("cant connect to balance")
            return None

    def get_account(self):

        return None

    def get_sum(self):
        json_data = self.get_api_data()
        accounts_list = [0]
        for acc in json_data['rows']:
            accounts_list.append(acc['balance'] / 100)
        self.logger.info("Balance successfully downloaded")
        return sum(accounts_list)


if __name__ == '__main__':
    connector = ConnMSBalance()

