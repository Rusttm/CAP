from PgsqlAlchemy.ConnMS.ConnMSMainClass import ConnMSMainClass
import datetime


class ConnMSCustBal(ConnMSMainClass):
    """ connector to MoiSklad customers balances"""
    request_tag = 'url_customers_bal_list'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""


    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_tag, token_conf_key=self.request_token)

    def get_cust_bal_rows_list(self, from_date: datetime = None, to_date: datetime = None, to_file=False) -> list:
        """ return list with dicts of customers balances
        has 'to_date' parameter
        date format '2022-12-08' or '2019-07-10 12:00:00'"""
        param = ""
        if from_date or to_date:
            if from_date:
                param = f"filter=updated>={from_date}"
            if to_date:
                param += f"&filter=updated<={to_date}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified to_date parameter")
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)

        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=data_dict, file_name=f"{self.request_tag}.json")
        return data_dict.get("rows", None)


if __name__ == '__main__':
    connector = ConnMSCustBal()
    data = connector.get_cust_bal_rows_list(to_file=True)
    print(data)
