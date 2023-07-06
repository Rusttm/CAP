from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSCorr(ConnMSMainClass):
    """get corrections balance"""
    request_url = 'url_customer_bal_corr_list'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""
    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    def get_corrections(self, to_file=False):
        """ return stores dictionary """
        return self.get_api_data(to_file=to_file)

    def get_correction_filtered_by_date(self, from_date=None, to_date=None, to_file=False):
        """ filterred by date from to or just
        date format '2022-12-08'  or '2019-07-10 12:00:00'"""
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
        result = self.get_api_data(to_file=to_file)
        return result


if __name__ == '__main__':
    connector = ConnMSCorr()
    connector.get_corrections(to_file=True)
    data = connector.get_correction_filtered_by_date(from_date="2023-01-01", to_date="2023-07-01", to_file=True)
    print(data)
