from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSStores(ConnMSMainClass):
    """get stores"""
    request_url = 'url_stock_all'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""
    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)
        # self.set_config()

    # def set_config(self):
    #     """ sets api_url and api_token from config file"""
    #     conf = self.get_config_data()
    #     if conf:
    #         self.set_api_url(conf['MoiSklad']['url_stores'])
    #         self.set_api_token(conf['MoiSklad']['access_token'])
    #     else:
    #         self.logger.warning("cant get info from configfile url or access_token")

    def get_stores(self, to_file=False):
        """ return stores dictionary """
        return self.get_api_data(to_file=to_file)


if __name__ == '__main__':
    connector = ConnMSStores()
    connector.get_stores(to_file=True)