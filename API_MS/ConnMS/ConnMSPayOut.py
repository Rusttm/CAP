from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSPayOut(ConnMSMainClass):
    """class to connect payments out"""
    request_url = 'url_outpayments_list'
    request_token = 'access_token'

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        # self.set_config()
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    # def set_config(self):
    #     """ sets api_url and api_token from config file"""
    #     conf = self.get_config_data()
    #     if conf:
    #         self.set_api_url(conf['MoiSklad']['url_outpayments_list'])
    #         self.set_api_token(conf['MoiSklad']['access_token'])
    #     else:
    #         self.logger.warning("cant get info from configfile url or access_token")

    def get_payout_data(self, to_file=False):
        """ return full payouts data """
        return self.get_api_data(to_file=to_file)

    def get_payout_filtered_by_date(self, from_date=None, to_date=None, to_file=False):
        """ filterred by date from to or just
        date format '2022-12-08'  or '2019-07-10 12:00:00'"""
        param = ""
        if from_date or to_date:
            if from_date:
                param = f"filter=moment>={from_date}"
            if to_date:
                param += f"&filter=moment<={to_date}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified from_date={from_date} "
                                f"and to_date={to_date} parameter")
            return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        return self.get_api_data(to_file=to_file)


if __name__ == '__main__':
    connector = ConnMSPayOut()
