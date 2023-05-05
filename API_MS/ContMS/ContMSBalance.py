from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSBalance import ConnMSBalance


class ContMSBalance(ContMSMainClass):
    """ controller for MoiSklad balance
    get info from configfile and request information
    from ConnMSBalance connector
    return sum of accounts balance
    and return {dictionary account:bal}"""
    connector = None

    def __init__(self):
        super().__init__()
        self.connector = ConnMSBalance()

    def get_config(self):
        """ return (url, token) from config file"""
        conf = self.get_config_data()
        if conf:
            url_balance = conf['MoiSklad']['url_money']
            access_token = conf['MoiSklad']['access_token']
            return url_balance, access_token
        else:
            return None, None

    def get_sum(self):
        """ getting sum accounts from balance connector"""
        # connector = ConnMSBalance()
        url, token = self.get_config()
        self.connector.set_api_config(api_url=url, api_token=token, to_file=False)
        sum_accounts = self.connector.get_sum()
        return sum_accounts

    def get_account_bal(self):
        """ getting accounts balances from balance connector"""
        # connector = ConnMSBalance()
        url, token = self.get_config()
        self.connector.set_api_config(api_url=url, api_token=token, to_file=False)
        bal_accounts = self.connector.get_accounts_bal()
        return bal_accounts


if __name__ == '__main__':
    controller = ContMSBalance()
    balance_sum = controller.get_sum()
    print(balance_sum)
    balance_acc = controller.get_account_bal()
    print(balance_acc)
