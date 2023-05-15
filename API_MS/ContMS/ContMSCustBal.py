from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSCustBal import ConnMSCustBal

class ContMSCustBal(ContMSMainClass, ConnMSCustBal):
    """ controller for MoiSklad customers balances sum
    and by groups"""
    connector = None
    file_name = "customers_dict.json"
    """ customers.json - default file name for stores dict"""
    sum_file_name = "customers_bal_sum.json"
    """ customers_bal_sum.json - default file name for stores with summary sum"""

    def __init__(self):
        super().__init__()
        # self.connector = ConnMSStockRemains()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSCustBal()
    groups = controller.get_cust_bal(to_file=True, to_date="2023-01-01")
    print(groups['sum'])
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
