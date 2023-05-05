from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSStockRemains import ConnMSStockRemains


class ContMSStockRemains(ContMSMainClass):
    """ controller for MoiSklad stock remains by product"""
    connector = None

    def __init__(self):
        super().__init__()
        self.connector = ConnMSStockRemains()
        self.logger.debug("module ContMSStockRemains started")

    def get_stock_remains(self, to_file=False):
        """ getting stock remains"""
        stock = self.connector.get_stock_remains(to_file=to_file)
        return stock

    def get_stock_remains_sum(self):
        """ getting stock remains"""
        stock_sum = self.connector.get_stock_remains_sum()
        return stock_sum


if __name__ == '__main__':
    controller = ContMSStockRemains()
    stock_sum = controller.get_stock_remains_sum()
    print(stock_sum)
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
