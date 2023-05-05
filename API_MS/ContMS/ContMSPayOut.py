from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSPayOut import ConnMSPayOut
import json

class ContMSPayOut(ContMSMainClass):
    """ controller class to get PaymentsOut data"""
    connector=None
    def __init__(self):
        super().__init__()
        self.connector = ConnMSPayOut()
        self.logger.debug("module ContMSPayOut started")

    # def get_config(self):
    #     """ return (url, token) from config file"""
    #     conf = self.get_config_data()
    #     if conf:
    #         url_payout = conf['MoiSklad']['url_outpayments_list']
    #         access_token = conf['MoiSklad']['access_token']
    #         return url_payout, access_token
    #     else:
    #         self.logger.warning("cant get info from configfile url_payout or access_token")
    #         return None, None

    def get_payout_data(self):
        """ return full payouts data """
        # connector = ConnMSPayOut()
        # url, token = self.get_config()
        # self.connector.set_api_config(api_url=url, api_token=token, to_file=False)
        payouts = self.connector.get_api_data()
        return payouts

    def get_payout_filtered_by_date(self, from_date=None, to_date=None):
        """ filterred by date from to or just
        date format '2022-12-08' """
        # connector = ConnMSPayOut()
        # url, token = self.get_config()
        # self.connector.set_api_config(api_url=url, api_token=token, to_file=False)
        param = ""
        if from_date or to_date:
            if from_date:
                param = f"filter=moment>={from_date}"
            if to_date:
                param += f"&filter=moment<={to_date}"
        else:
            self.logger.warning("paymentsOut request not specified from_date or to_date parameter")
            return self.connector.get_api_data()
        self.connector.set_api_param_line(param)
        payouts = self.connector.get_api_data()
        # FILE_PATH = "payouts_full.json"
        # with open(FILE_PATH, 'w') as ff:
        #     json.dump(payouts, ff, ensure_ascii=False)
        return payouts


if __name__ == '__main__':
    controller = ContMSPayOut()
    data = controller.get_payout_filtered_by_date()
    # print(data)
    # balance_acc = controller.get_account_bal()
    # print(balance_acc)
