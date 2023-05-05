from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSPayIn(ConnMSMainClass):
    """class to connect payments out"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ConnMSPayIn started")
        self.set_config()

    def set_config(self):
        """ sets api_url and api_token from config file"""
        conf = self.get_config_data()
        if conf:
            self.set_api_url(conf['MoiSklad']['url_inpayments_list'])
            self.set_api_token(conf['MoiSklad']['access_token'])
        else:
            self.logger.warning("cant get info from configfile url_balance or access_token")


if __name__ == '__main__':
    connector = ConnMSPayIn()
