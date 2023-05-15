from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSProdList import ConnMSProdList
# import json


class ContMSProdList(ContMSMainClass, ConnMSProdList):
    """ controller class to get inner invoices data"""
    connector = None

    def __init__(self):
        super().__init__()
        # self.connector = ConnMSPayIn()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSProdList()
    data = controller.get_prod_list_filtered_by_updated(from_date="2023-01-01", to_date="2023-02-01", to_file=True)
    print(data)

