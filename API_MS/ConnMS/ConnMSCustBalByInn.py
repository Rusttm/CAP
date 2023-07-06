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
    used_requests = {"positive": ['url_inpayments_list', 'url_inpack_list'],
                     "negative": ['url_outpayments_list', 'url_outpack_list']}



    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")

    def get_cust_bal_on_date(self, inn: str = None, on_date: str = None, to_file: bool = False) -> float:
        """ general function to count client bal on date"""
        transactions_list = list()
        current_bal_dict = self.get_cust_cur_bal_dict(inn=inn)
        customer_id = current_bal_dict.get("customer_id", None)
        for req_tag in self.used_requests.get("positive", []):
            transactions = self.request_data_by_inn(req_tag=req_tag, customer_id=customer_id, positive=True)
            # print(f"from {req_tag} ({len(transactions)}) transactions {sorted(transactions, key=lambda x:x[0])}")
            transactions_list.extend(transactions)
        for req_tag in self.used_requests.get("negative", []):
            transactions = self.request_data_by_inn(req_tag=req_tag, customer_id=customer_id, positive=False)
            # print(f"from {req_tag} ({len(transactions)}) transactions {sorted(transactions, key=lambda x:x[0])}")
            transactions_list.extend(transactions)
        transactions = self.get_cust_corr_bal_list(customer_id=customer_id)
        transactions_list.extend(transactions)
        # print(transactions_list)
        result = self.count_bal_on_date(transactions_list=transactions_list, on_date=on_date)
        if current_bal_dict.get('customer_cur_bal', None)!=result:
            print(f"current balance client {current_bal_dict.get('customer_inn', None)} not matched with counted")
            print(f"current balance={current_bal_dict.get('customer_cur_bal', None)} counted balance={result}")
        return result


    def count_bal_on_date(self, transactions_list: list = None, on_date: str = None) -> float:
        """ count balance from client transactions list"""
        sorted_transactions_list = sorted(transactions_list, key=lambda x:x[0])
        result = 0
        for date, transaction_sum in sorted_transactions_list:
            if datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f") <= datetime.datetime.strptime(on_date, "%Y-%m-%d %H:%M:%S.%f"):
                result += transaction_sum
            else:
                break
        return round(result, 2)
    def get_cust_cur_bal_dict(self, inn: str = None, to_file: bool = False) -> dict:
        """ return dict {"customer_bal": 0, "customer_inn": inn, "customer_href": str, "customer_id": str}"""
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
        new_data_dict = dict({"customer_cur_bal": 0, "customer_inn": inn, "customer_href": str})
        if data_dict["meta"].get("size", None):
            for i, prod in enumerate(data_dict["rows"]):
                bal = prod["balance"] / 100
                new_data_dict.update({"customer_cur_bal": round(new_data_dict.get("balance", 0) + bal, 2)})
                new_data_dict.update({"customer_href": prod["meta"]["href"]})
                new_data_dict.update({"customer_id": prod["counterparty"]["id"]})
        else:
            print(f"no data in requested {request_url}")

        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=new_data_dict, file_name="customers_bal_inn_sum.json")
        return new_data_dict

    def get_cust_corr_bal_list(self, customer_id: str = None, to_file: bool = False) -> dict:
        """ list of corrections in client balance
        return list"""
        customer_href = f"https://online.moysklad.ru/api/remap/1.2/entity/counterparty/{customer_id}"
        request_url = 'url_customer_bal_corr_list'
        param = ""
        res_list = list()
        if customer_href:
            if customer_href:
                param = f"filter=agent={customer_href}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified customer_href parameter")
        super().set_config(url_conf_key=request_url, token_conf_key=self.request_token)
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)
        if data_dict["meta"].get("size", None):
            for i, prod in enumerate(data_dict["rows"]):
                res_list.append((prod.get('moment', None), prod.get('sum', 0) / 100))
        else:
            print(f"no data in requested {request_url}")

        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=data_dict, file_name="customers_bal_inn_sum.json")
        return res_list

    def request_data_by_inn(self, customer_id: str = None, req_tag: str = None, to_file: bool = False, positive: bool = True):
        customer_href = f"https://online.moysklad.ru/api/remap/1.2/entity/counterparty/{customer_id}"
        param = ""
        if customer_href:
            if customer_href:
                param = f"filter=agent={customer_href}"
        else:
            self.logger.warning(f"{__class__.__name__} request not specified customer_meta parameter")
        super().set_config(url_conf_key=req_tag, token_conf_key=self.request_token)
        self.set_api_param_line(param)
        data_dict = self.get_api_data(to_file=to_file)
        # hundler
        if positive:
            flag = 1
        else:
            flag = -1
        res_list = list()
        # needs exceptions
        try:
            for i, prod in enumerate(data_dict["rows"]):
                res_list.append((prod.get('moment', None), flag * prod.get('sum', 0) / 100))
        except KeyError as e:
            print(f"cant take data from {req_tag} for {customer_href}, error: KeyError {e}")

        # if write in file
        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
            ConnMSSaveJson().save_data_json_file(data_dict=data_dict, file_name="customers_bal_inn_sum.json")

        return res_list


    def print_date(self):
        print(self.right_date)


if __name__ == '__main__':
    connector = ConnMSCustBal()
    # data = connector.get_cust_cur_bal_dict(inn='5403362299')
    data = connector.get_cust_bal_on_date(inn='5403362299', on_date="2023-07-6 23:59:00.000")
    print(data)
    # print(data.get("customer_href", None))
    # data = connector.get_payments_in_cust(customer_id='https://online.moysklad.ru/api/remap/1.2/entity/counterparty/3257c64d-5783-11eb-0a80-06ec00b865d5', to_file=True)
    # print(data)
    # print(data.get('customer_payments_in', None))
    # print(connector.right_date)
