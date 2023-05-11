from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSStockRemains import ConnMSStockRemains


class ContMSStockRemains(ContMSMainClass, ConnMSStockRemains):
    """ controller for MoiSklad stock remains by product"""
    connector = None

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSStockRemains()
    stock_remains = controller.get_stock_remains(to_date="2022-12-08")
    print(stock_remains["sum"])
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
