from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass



class ConnMSCustBal(ConnMSMainClass):
    """ connector to MoiSklad customers balances"""
    request_url = 'url_customers_bal_list'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    def get_cust_bal(self, from_date=None, to_date=None, to_file=False):
        """ return dict with customers balances and sum
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
            # self.set_api_param_line(param)
            # return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)
        new_data_dict = dict({"sum": 0.0, "customers": data_dict})
        for i, prod in enumerate(data_dict["rows"]):
            bal = prod["balance"] / 100
            new_data_dict["sum"] = round(new_data_dict.get("sum", 0) + bal, 2)
            # if sum_prod > 1000000:
            #     print(f"{i=}, {prod['name']}, {cost=} * {num=} = {sum_prod=}")
        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=new_data_dict, file_name="customers_bal_sum.json")
        return new_data_dict


if __name__ == '__main__':
    connector = ConnMSCustBal()
    data = connector.get_cust_bal(to_file=True)
    print(data["sum"])
