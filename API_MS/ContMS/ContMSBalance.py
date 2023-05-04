from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSBalance import ConnMSBalance
import configparser
import logging
import os


class ContMSBalance(ContMSMainClass):
    """ controller for MoiSklad balance
    get info from configfile and request information
    from ConnMSBalance connector
    return sum of acccounts balance
    and return {dictionary account:bal}"""

    def __init__(self):
        super().__init__()

    def get_config(self):
        """ return data from config file"""
        try:
            conf = configparser.ConfigParser()
            CONF_FILE_PATH = os.path.join(os.path.dirname(os.getcwd()), "config", "config.ini")
            if not os.path.exists(CONF_FILE_PATH):
                self.logger.error(f"config file {CONF_FILE_PATH} doesnt exist")
            conf.read(CONF_FILE_PATH)
            url_balance = conf['MoiSklad']['url_money']
            access_token = conf['MoiSklad']['access_token']
            self.logger.info("got info from configfile")
            return (url_balance, access_token)
        except Exception as e:
            self.logger.error("Cant read file", e)
            print(e)
            return (None, None)
        return None

    def get_sum(self):
        """ getting sum accounts from balance connector"""
        connector = ConnMSBalance()
        url, token = self.get_config()
        connector.set_api_config(api_url=url, api_token=token, to_file=False)
        sum_accounts = connector.get_sum()
        return sum_accounts

    def get_account_bal(self):
        """ getting sum accounts from balance connector"""
        connector = ConnMSBalance()
        url, token = self.get_config()
        connector.set_api_config(api_url=url, api_token=token, to_file=False)
        bal_accounts = connector.get_accounts_bal()
        return bal_accounts


if __name__ == '__main__':
    controller = ContMSBalance()
    balance_sum = controller.get_sum()
    print(balance_sum)
    balance_acc = controller.get_account_bal()
    print(balance_acc)
