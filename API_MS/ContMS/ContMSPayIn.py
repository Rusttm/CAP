from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSPayIn import ConnMSPayIn
# import json


class ContMSPayIn(ContMSMainClass, ConnMSPayIn):
    """ controller class to get PaymentsIn data"""
    connector = None

    def __init__(self):
        super().__init__()
        # self.connector = ConnMSPayIn()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSPayIn()
    data = controller.get_payin_filtered_by_date(from_date="2023-01-01", to_date="2023-02-01", to_file=True)
    # data = controller.get_payin_filtered_by_date()
    # print(data)
    # balance_acc = controller.get_account_bal()
    # print(balance_acc)
