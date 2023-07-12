from PgsqlAlchemy.ConnMS.ConnMSMainClass import ConnMSMainClass
import datetime


class ConnMSFilter(ConnMSMainClass):
    """ connector to MoiSklad customers balances with filters"""
    request_tag = 'url_customers_bal_list'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""


    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")

    def get_ms_request_with_date_filter(self, from_date: datetime = None,
                                        to_date: datetime = None,
                                        filter_field_name: str = None,
                                        url_table_name: str = None) -> list:
        """ return list with dicts of customers balances
        has 'to_date' parameter
        date format '2022-12-08' or '2019-07-10 12:00:00'"""
        super().set_config(url_conf_key=url_table_name, token_conf_key=self.request_token)
        param = ""
        if filter_field_name:
            if from_date or to_date:
                if from_date:
                    if filter_field_name == "momentFrom_momentTo":
                        param = f"{filter_field_name}From>={from_date}"
                    elif filter_field_name == "on_moment":
                        param = ""
                    else:
                        param = f"filter={filter_field_name}>={from_date}"
                if to_date:
                    if filter_field_name == "momentFrom_momentTo":
                        param += f"&{filter_field_name}To>={from_date}"
                    elif filter_field_name == "on_moment":
                        param += f"{filter_field_name}={from_date}"
                    else:
                        param += f"&filter={filter_field_name}<={to_date}"
            else:
                self.logger.warning(f"{__class__.__name__} request not specified to_date parameter")
        super().set_api_param_line(param)
        data_dict = self.get_api_data()
        return data_dict.get("rows", None)


if __name__ == '__main__':
    connector = ConnMSFilter()
    data = connector.get_ms_request_with_date_filter(url_table_name='url_customers_bal_list')
    print(f"got {len(data)} rows")
    data = connector.get_ms_request_with_date_filter(url_table_name='url_customer_bal_corr_list')
    print(f"got {len(data)} rows")

