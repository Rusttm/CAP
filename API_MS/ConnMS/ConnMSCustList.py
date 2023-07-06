from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSCustList(ConnMSMainClass):
    """class to connect customers list """
    request_url = 'url_customers_list'
    request_token = 'access_token'

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    def get_custom_list_filtered_by_updated(self, from_date=None, to_date=None, to_file=False):
        """ filterred by date from to or just
        date format '2022-12-08' or '2019-07-10 12:00:00'"""
        param = ""
        if from_date or to_date:
            if from_date:
                param = f"filter=updated>={from_date}"
            if to_date:
                param += f"&filter=updated<={to_date}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified from_date={from_date} and to_date={to_date} parameter")
            return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        payouts = self.get_api_data(to_file=to_file)
        return payouts

    def get_prod_list_filtered_by_create(self, from_date=None, to_date=None, to_file=False):
        """ filterred by create from to or just
        date format '2022-12-08' """
        param = ""
        if from_date or to_date:
            if from_date:
                param = f"filter=moment>={from_date}"
            if to_date:
                param += f"&filter=moment<={to_date}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified from_date={from_date} and to_date={to_date} parameter")
            return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        # prod_list = self.get_api_data(to_file=to_file)
        return self.get_api_data(to_file=to_file)

if __name__ == '__main__':
    connector = ConnMSCustList()
    custom = connector.get_custom_list_filtered_by_updated(to_file=True)
    print(custom)