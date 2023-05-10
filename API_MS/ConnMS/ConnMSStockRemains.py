from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSStockRemains(ConnMSMainClass):
    """ connector to MoiSklad stock remains(ненулевые остатки)"""
    request_url = 'url_stock_all'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ConnMSStockRemains started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)
        # self.set_config()

    # def set_config(self):
    #     """ sets api_url and api_token from config file"""
    #     conf = self.get_config_data()
    #     if conf:
    #         self.set_api_url(conf['MoiSklad']['url_stock_all'])
    #         self.set_api_token(conf['MoiSklad']['access_token'])
    #     else:
    #         self.logger.warning("cant get info from configfile url or access_token")

    def get_stock_remains(self, to_date=None, to_file=False):
        """ return dict with stock remains"""
        param = "filter=quantityMode=all"
        if to_date:
            param += f"&filter=moment={to_date}"
        else:
            self.logger.warning("StockRemains request not specified to_date parameter")
            self.set_api_param_line(param)
            return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        new_data_dict = self.get_api_data(to_file=to_file)
        return new_data_dict



if __name__ == '__main__':
    connector = ConnMSStockRemains()
    connector.get_stock_remains(to_file=True)
