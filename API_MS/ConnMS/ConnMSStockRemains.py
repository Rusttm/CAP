from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSStockRemains(ConnMSMainClass):
    """ connector to MoiSklad stock remains(ненулевые остатки)"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ConnMSStockRemains started")
        self.set_config()

    def set_config(self):
        """ sets api_url and api_token from config file"""
        conf = self.get_config_data()
        if conf:
            self.set_api_url(conf['MoiSklad']['url_stock_all'])
            self.set_api_token(conf['MoiSklad']['access_token'])
        else:
            self.logger.warning("cant get info from configfile url or access_token")

    def get_stock_remains(self, to_date=None, to_file=False):
        """ return dict with stock remains"""
        param = ""
        if to_date:
            param += f"filter=moment={to_date}"
        else:
            self.logger.warning("StockRemains request not specified to_date parameter")
            return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        new_data_dict = self.get_api_data(to_file=to_file)
        return new_data_dict

    # def get_stock_remains_sum(self, to_date=None):
    #     data_dict = self.get_stock_remains(to_date=to_date)
    #     result_sum = 0
    #     if data_dict:
    #         for prod in data_dict['rows']:
    #             try:
    #                 result_sum += prod['stock'] * prod['price']
    #             except Exception as e:
    #                 self.logger.warning(f"for {prod['name']} summ not considered. error {e}")
    #     return result_sum


if __name__ == '__main__':
    connector = ConnMSStockRemains()
    connector.get_stock_remains(to_file=True)
