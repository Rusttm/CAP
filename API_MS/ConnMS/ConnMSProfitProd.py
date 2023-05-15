from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass



class ConnMSProfitProd(ConnMSMainClass):
    """ connector to MoiSklad profit by products"""
    request_url = 'url_profit_by_prod_list'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    def get_profit_by_prod(self, from_date=None, to_date=None, to_file=False):
        """ return dict with profit by products
        has 'to_date' parameter
        date format '2022-12-08' or '2019-07-10 12:00:00'"""
        param = ""
        if from_date or to_date:
            if from_date:
                param = f"momentFrom={from_date}"
            if to_date:
                param += f"&momentTo<={to_date}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified to_date parameter")
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)
        new_data_dict = dict({"sum": 0.0, "products": data_dict})
        for i, prod in enumerate(data_dict["rows"]):
            # profit - прибыль
            profit = prod["profit"] / 100
            # margin -рентабельность
            margin = prod["margin"]
            new_data_dict["sum"] = round(new_data_dict.get("sum", 0) + profit, 2)
        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=new_data_dict, file_name="profit_prod_sum.json")
        return new_data_dict


if __name__ == '__main__':
    connector = ConnMSProfitProd()
    data = connector.get_profit_by_prod(from_date="2023-05-01", to_date="2023-05-15", to_file=True)
    print(data["sum"])
