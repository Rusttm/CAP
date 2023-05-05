from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSPayIn import ConnMSPayIn
# import json


class ContMSPayIn(ContMSMainClass):
    """ controller class to get PaymentsIn data"""
    connector = None

    def __init__(self):
        super().__init__()
        self.connector = ConnMSPayIn()
        self.logger.debug("module ContMSPayIn started")

    def get_payin_data(self):
        """ return full payouts data """
        payouts = self.connector.get_api_data()
        return payouts

    def get_payin_filtered_by_date(self, from_date=None, to_date=None, to_file=False):
        """ filterred by date from to or just
        date format '2022-12-08' """
        return self.connector.get_payin_filtered_by_date(from_date=from_date, to_date=to_date, to_file=to_file)

    def get_payin_filtered_by_create(self, from_date=None, to_date=None, to_file=False):
        return self.connector.get_payin_filtered_by_create(from_date=from_date, to_date=to_date, to_file=to_file)


if __name__ == '__main__':
    controller = ContMSPayIn()
    data = controller.get_payin_filtered_by_date(from_date="2023-01-01", to_date="2023-02-01", to_file=True)
    # data = controller.get_payin_filtered_by_date()
    # print(data)
    # balance_acc = controller.get_account_bal()
    # print(balance_acc)
