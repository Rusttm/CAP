from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSPackOut(ConnMSMainClass):
    """class to connect outer packlists"""
    request_url = 'url_outpack_list'
    request_token = 'access_token'

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    def get_packout_filtered_by_date(self, from_date=None, to_date=None, to_file=False):
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
        packouts = self.get_api_data(to_file=to_file)
        return packouts

    def get_packout_filtered_by_create(self, from_date=None, to_date=None, to_file=False):
        """ filterred by create from to or just
        date format '2022-12-08' """
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
        payouts = self.get_api_data(to_file=to_file)
        return payouts

if __name__ == '__main__':
    connector = ConnMSPackOut()
    print(connector.get_packout_filtered_by_date(from_date="2023-01-01", to_date="2023-02-01", to_file=True))