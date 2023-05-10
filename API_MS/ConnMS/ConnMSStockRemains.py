from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass
from API_MS.ConnMS.ConnMSSaveFile import ConnMSSaveFile


class ConnMSStockRemains(ConnMSMainClass, ConnMSSaveFile):
    """ connector to MoiSklad stock remains(ненулевые остатки)"""
    request_url = 'url_stock_all'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    def get_stock_remains(self, to_date=None, to_file=False):
        """ return dict with stock remains"""
        param = "filter=quantityMode=all"
        if to_date:
            param += f"&filter=moment={to_date}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified to_date parameter")
            # self.set_api_param_line(param)
            # return self.get_api_data(to_file=to_file)
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)
        new_data_dict = dict({"sum": 0.0, "stock": data_dict})
        for i, prod in enumerate(data_dict["rows"]):
            cost = prod["price"] / 100
            num = prod["stock"]
            sum_prod = round(cost * num, 2)
            new_data_dict["sum"] = round(new_data_dict.get("sum", 0) + sum_prod, 2)
            # if sum_prod > 1000000:
            #     print(f"{i=}, {prod['name']}, {cost=} * {num=} = {sum_prod=}")
        if to_file:
            ConnMSSaveFile().save_data_json_file(data_dict=new_data_dict, file_name="remains_sum.json")
        return new_data_dict


if __name__ == '__main__':
    connector = ConnMSStockRemains()
    data = connector.get_stock_remains(to_file=True)
    print(data["sum"])
