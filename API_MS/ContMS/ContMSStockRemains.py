from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSStockRemains import ConnMSStockRemains


class ContMSStockRemains(ContMSMainClass):
    """ controller for MoiSklad stock remains by product"""
    connector = None

    def __init__(self):
        super().__init__()
        self.connector = ConnMSStockRemains()
        self.logger.debug("module ContMSBalance started")

    def get_stock_remains(self, to_file=False):
        """ getting stock remains"""
        sum_accounts = self.connector.get_stock_remains(to_file=to_file)
        return sum_accounts

    def get_account_bal(self):
        """ getting stock remains sum"""
        bal_accounts = self.connector.get_stock_remains_sum()
        return bal_accounts


if __name__ == '__main__':
    controller = ContMSStockRemains()
    stock_sum = controller.get_account_bal()
    print(balance_sum)
    stock = controller.get_account_bal()
    print(stock)
