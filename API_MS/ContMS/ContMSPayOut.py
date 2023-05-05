from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSPayOut import ConnMSPayOut


class ContMSPayOut(ContMSMainClass):
    """ controller class to get PaymentsOut data"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ContMSPayOut started")

    def get_config(self):
        """ return (url, token) from config file"""
        conf = self.get_config_data()
        if conf:
            url_payout = conf['MoiSklad']['url_outpayments_list']
            access_token = conf['MoiSklad']['access_token']
            return url_payout, access_token
        else:
            return None, None

    def get_payout_data(self):
        """ return full payouts data """
        connector = ConnMSPayOut()
        url, token = self.get_config()
        connector.set_api_config(api_url=url, api_token=token, to_file=False)
        payouts = connector.get_api_data()
        return payouts

    def get_payout_filtered_by_date(self, from_date=None, to_date=None):
        """ filterred by date from to or just
        date format '2022-12-08' """
        connector = ConnMSPayOut()
        url, token = self.get_config()
        connector.set_api_config(api_url=url, api_token=token, to_file=False)
        param = ""
        if from_date:
            param = f"filter=moment>={from_date}"
            if to_date:
                param += f"&filter=moment<={to_date}"
        else:
            self.logger.error("not specified 'from_date' parameter")
        connector.set_api_param_line(param)
        payouts = connector.get_api_data()
        # FILE_PATH = "payouts5.json"
        # with open(FILE_PATH, 'w') as ff:
        #     json.dump(payouts, ff, ensure_ascii=False)
        return payouts


if __name__ == '__main__':
    controller = ContMSPayOut()
    data = controller.get_payout_filtered_by_date(from_date="2023-01-01", to_date="2023-02-01")
    # print(data)
    # balance_acc = controller.get_account_bal()
    # print(balance_acc)
