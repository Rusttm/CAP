from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSStockByStore(ConnMSMainClass):
    """ connector to MoiSklad stock remains(ненулевые остатки) products by store"""
    request_url = 'url_stock_stores'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""
    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)
        # self.set_config()

    def get_stock_by_store(self, to_date=None, to_file=False):
        """ return dict with stock products with store remains"""
        param = ""
        if to_date:
            param += f"filter=moment={to_date}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified to_date parameter")
            return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        new_data_dict = self.get_api_data(to_file=to_file)
        return new_data_dict


if __name__ == '__main__':
    connector = ConnMSStockByStore()
    data = connector.get_stock_by_store(to_file=True)
    print(data)
