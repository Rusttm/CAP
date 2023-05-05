from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSPayOut import ConnMSPayOut
import json

class ContMSPayOut(ContMSMainClass):
    """ controller class to get PaymentsOut data"""
    connector = None

    def __init__(self):
        super().__init__()
        self.connector = ConnMSPayOut()
        self.logger.debug("module ContMSPayOut started")

    def get_payout_data(self):
        """ return full payouts data """
        return self.connector.get_payout_data()

    def get_payout_filtered_by_date(self, from_date=None, to_date=None, to_file=False):
        """ filterred by date from to or just
        date format '2022-12-08' """
        return self.connector.get_api_data(from_date=from_date, to_date=to_date, to_file=to_file)


if __name__ == '__main__':
    controller = ContMSPayOut()
    data = controller.get_payout_filtered_by_date()
    # print(data)
    # balance_acc = controller.get_account_bal()
    # print(balance_acc)
