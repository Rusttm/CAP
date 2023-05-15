from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSProfitProd import ConnMSProfitProd
# import json


class ContMSProfitProd(ContMSMainClass, ConnMSProfitProd):
    """ controller class to get out invoices data"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSProfitProd()
    data = controller.get_profit_by_prod(from_date="2023-01-01", to_date="2023-02-01", to_file=True)
    print(data['sum'])
