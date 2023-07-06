import datetime

from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSCustBal(ConnMSMainClass):
    """ connector to MoiSklad customers balances"""
    request_url = 'url_customers_bal_list'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""
    left_date = '2018-10-01 00:00:00'
    right_date = f"{datetime.datetime.now().strftime('%Y-%m-%d')} 24:00:00"

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")


    def get_cust_cur_bal_dict(self, inn: str = None, to_file: bool = False) -> dict:
        """ return dict with customer_balance and customer_inn"""
        request_url = 'url_customers_bal_list'
        param = ""
        if inn:
            if inn:
                param = f"filter=counterparty.inn={inn}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified inn parameter")
            # self.set_api_param_line(param)
            # return self.get_api_data(to_file=to_file)
        super().set_config(url_conf_key=request_url, token_conf_key=self.request_token)
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)
        new_data_dict = dict({"customer_bal": 0, "customer_inn": inn, "customer_href": str})
        for i, prod in enumerate(data_dict["rows"]):
            bal = prod["balance"] / 100
            new_data_dict["customer_bal"] = round(new_data_dict.get("balance", 0) + bal, 2)
            # new_data_dict["customer_meta"] = prod["meta"]
            new_data_dict["customer_href"] = prod["meta"]["href"]
        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=new_data_dict, file_name="customers_bal_inn_sum.json")
        return new_data_dict

    def get_payments_in_cust(self, customer_href: str = None,to_file: bool = False):
        """ return dict with customer_balance and customer_inn"""
        request_url = 'url_inpayments_list'
        param = ""
        if customer_href:
            if customer_href:
                param = f"filter=agent={customer_href}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified customer_meta parameter")

        super().set_config(url_conf_key=request_url, token_conf_key=self.request_token)
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)

        res_list = list()
        for i, prod in enumerate(data_dict["rows"]):
            res_list.append((prod.get('moment', None), prod.get('sum', 0)/100))
            # bal = prod["balance"] / 100
            # new_data_dict["customer_bal"] = round(new_data_dict.get("balance", 0) + bal, 2)
            # new_data_dict["customer_meta"] = prod["meta"]
        new_data_dict = dict({"customer_payments_in": res_list, "customer_href": customer_href})
        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=new_data_dict, file_name="customers_bal_inn_sum.json")
        return new_data_dict
        pass

    def print_date(self):
        print(self.right_date)


if __name__ == '__main__':
    connector = ConnMSCustBal()
    data = connector.get_cust_cur_bal_dict(inn='5403362299', to_file=True)
    # print(data)
    # print(data.get("customer_href", None))
    data = connector.get_payments_in_cust(customer_href='https://online.moysklad.ru/api/remap/1.2/entity/counterparty/3257c64d-5783-11eb-0a80-06ec00b865d5', to_file=True)
    print(data.get('customer_payments_in', None))
    # print(connector.right_date)
