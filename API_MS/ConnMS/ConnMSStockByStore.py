from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSStockByStore(ConnMSMainClass):
    """ connector to MoiSklad stock remains(ненулевые остатки) by stores"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ConnMSStockByStore started")
        self.set_config()

    def set_config(self):
        """ sets api_url and api_token from config file"""
        conf = self.get_config_data()
        if conf:
            self.set_api_url(conf['MoiSklad']['url_store_stores'])
            self.set_api_token(conf['MoiSklad']['access_token'])
        else:
            self.logger.warning("cant get info from configfile url_balance or access_token")

    def get_stock_remains(self, to_file=False):
        """ return dict with stock remains"""
        data_dict = self.get_api_data(to_file=to_file)
        return data_dict

    def get_stock_remains_sum(self):
        data_dict = self.get_api_data()
        result_sum = 0
        if data_dict:
            for prod in data_dict['rows']:
                try:
                    result_sum += prod['stock'] * prod['price']
                except Exception as e:
                    self.logger.warning(f"for {prod['name']} summ not considered")
        return result_sum






if __name__ == '__main__':
    connector = ConnMSStockRemains()
