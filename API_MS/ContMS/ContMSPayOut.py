from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSPayOut import ConnMSPayOut
import json

class ContMSPayOut(ContMSMainClass, ConnMSPayOut):
    """ controller class to get PaymentsOut data"""
    connector = None

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSPayOut()
    data = controller.get_payout_filtered_by_date(to_file=True)
    # print(data)
    # balance_acc = controller.get_account_bal()
    # print(balance_acc)
