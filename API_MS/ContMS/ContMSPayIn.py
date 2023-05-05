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

    def get_config(self):
        """ return (url, token) from config file"""
        conf = self.get_config_data()
        if conf:
            url_payin = conf['MoiSklad']['url_inpayments_list']
            access_token = conf['MoiSklad']['access_token']
            return url_payin, access_token
        else:
            self.logger.warning("cant get info from configfile url_payin or access_token")
            return None, None

    def get_payin_data(self):
        """ return full payouts data """
        # self.connector = ConnMSPayOut()
        url, token = self.get_config()
        self.connector.set_api_config(api_url=url, api_token=token, to_file=False)
        payouts = self.connector.get_api_data()
        return payouts

    def get_payin_filtered_by_date(self, from_date=None, to_date=None):
        """ filterred by date from to or just
        date format '2022-12-08' """
        # connector = ConnMSPayOut()
        url, token = self.get_config()
        self.connector.set_api_config(api_url=url, api_token=token, to_file=False)
        param = ""
        if from_date or to_date:
            if from_date:
                param = f"filter=moment>={from_date}"
            if to_date:
                param += f"&filter=moment<={to_date}"
        else:
            self.logger.warning("paymentsIn request not specified from_date or to_date parameter")
            return self.connector.get_api_data()
        self.connector.set_api_param_line(param)
        payouts = self.connector.get_api_data()
        # FILE_PATH = "payin_filtered.json"
        # with open(FILE_PATH, 'w') as ff:
        #     json.dump(payouts, ff, ensure_ascii=False)
        return payouts

    def get_payin_filtered_by_create(self, from_date=None, to_date=None):
        """ filterred by create from to or just
        date format '2022-12-08' """
        # connector = ConnMSPayOut()
        url, token = self.get_config()
        self.connector.set_api_config(api_url=url, api_token=token, to_file=False)
        param = ""
        if from_date:
            param = f"filter=created>={from_date} 00:00:00.000"
            if to_date:
                param += f"&filter=created<={to_date} 00:00:00.000"
        else:
            self.logger.error("not specified from_date parameter")
        self.connector.set_api_param_line(param)
        payouts = self.connector.get_api_data()
        # FILE_PATH = "payin_filtered.json"
        # with open(FILE_PATH, 'w') as ff:
        #     json.dump(payouts, ff, ensure_ascii=False)
        return payouts


if __name__ == '__main__':
    controller = ContMSPayIn()
    # data = controller.get_payin_filtered_by_date(from_date="2023-01-01", to_date="2023-02-01")
    data = controller.get_payin_filtered_by_date()
    # print(data)
    # balance_acc = controller.get_account_bal()
    # print(balance_acc)
