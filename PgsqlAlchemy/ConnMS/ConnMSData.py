from PgsqlAlchemy.ConnMS.ConnMSMainClass import ConnMSMainClass
import datetime


class ConnMSData(ConnMSMainClass):
    """ connector to MoiSklad customers balances with filters"""
    request_tag = 'url_customers_bal_list'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""


    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")

    def get_ms_request(self, url_table_name: str = None) -> list:
        """ return list with dicts"""
        super().set_config(url_conf_key=url_table_name, token_conf_key=self.request_token)
        data_dict = self.get_api_data()
        return data_dict.get("rows", None)


if __name__ == '__main__':
    connector = ConnMSData()
    data = connector.get_ms_request(url_table_name='url_customers_bal_list')
    print(f"got {len(data)} rows")
    # data = connector.get_ms_request(url_table_name='url_customer_bal_corr_list')
    # print(f"got {len(data)} rows")

