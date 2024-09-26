from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSProfitCust import ConnMSProfitCust
# import json


class ContMSProfitCust(ContMSMainClass, ConnMSProfitCust):
    """ controller class to get out invoices data"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSProfitCust()
    data = controller.get_profit_by_cust(from_date="2024-07-01", to_date="2024-07-31", to_file=True)
    print(data['sum'])
