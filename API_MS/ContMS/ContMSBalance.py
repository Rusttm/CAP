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
        self.logger.debug("module ContMSBalance started")

    def get_sum(self):
        """ getting sum accounts from balance connector"""
        sum_accounts = self.connector.get_sum()
        return sum_accounts

    def get_account_bal(self):
        """ getting accounts balances from balance connector"""
        bal_accounts = self.connector.get_accounts_bal()
        return bal_accounts


if __name__ == '__main__':
    controller = ContMSBalance()
    balance_sum = controller.get_sum()
    print(balance_sum)
    balance_acc = controller.get_account_bal()
    print(balance_acc)
