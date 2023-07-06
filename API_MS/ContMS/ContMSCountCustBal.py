from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSCustBal import ConnMSCustBal

class ContMSCountCustBal(ContMSMainClass, ConnMSCustBal):
    """ controller for MoiSklad count customers balances sum
    from invoices and payments"""
    connector = None


    def __init__(self):
        super().__init__()
        # self.connector = ConnMSStockRemains()
        self.logger.debug(f"module {__class__.__name__} started")

    def get_customer_current_bal(self, cust_inn='6452143816'):
        pass


if __name__ == '__main__':
    controller = ContMSCountCustBal()
    groups = controller.get_cust_bal(to_file=True, to_date="2023-01-01")
    print(groups['sum'])
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
