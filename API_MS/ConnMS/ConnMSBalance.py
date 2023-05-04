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
    entity_accounts = None

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
            # if write to file and checked to_file==True
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
                try:
                    # try to get entity accounts
                    entity = acc_req.json()['rows'][0]['organization']['meta']['href']
                    entity_accounts_href = entity + "/accounts/"
                    entity_accounts_req = requests.get(url=entity_accounts_href, headers=header_for_token_auth)
                    self.entity_accounts = entity_accounts_req.json()
                except Exception as e:
                    print(e)
                self.logger.info("balance requested successful")
                return acc_req.json()

        except IndexError:
            print('Cant read account data', Exception)
            logging.warning("cant connect to balance")
            return None

    def get_accounts_bal(self):
        """ return dict with acconts and balance
        example {'ПАО РОСБАНК (40702840997960000004)': 0.0, ..}"""
        json_data = self.get_api_data()
        entity_accounts = self.entity_accounts
        """ getting list of entuty accounts"""
        accounts_dict = dict()
        for i, acc in enumerate(json_data['rows']):
            if i != 0:
                try:
                    account_name = account_number = acc['account']['name']
                    for account in entity_accounts['rows']:
                        """ looking account number in entity account list"""
                        if account['accountNumber'] == account_number:
                            account_name = f"{account['bankName']} ({account_number})"
                    accounts_dict[account_name] = acc['balance'] / 100
                except Exception as e:
                    print(e)
        self.logger.info("Accounts sum successfully downloaded")
        return accounts_dict

    def get_sum(self):
        json_data = self.get_api_data()
        accounts_list = [0]
        for acc in json_data['rows']:
            accounts_list.append(acc['balance'] / 100)
        self.logger.info("Balance successfully downloaded")
        return sum(accounts_list)


if __name__ == '__main__':
    connector = ConnMSBalance()
