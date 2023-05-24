from API_MS.MSMainClass import MSMainClass


class MSMain(MSMainClass):
    """ this class gather all reports together """
    tables_dict = {"product_fields": "products_table",
                   "stockall_fields": "stock_remains_table",
                   "stockstore_fields": "stock_bystore_table",
                   "profit_byprod_fields": "profit_byprod_table",
                   "profit_bycust_fields": "profit_bycust_table",
                   "payins_fields": "payments_in_table",
                   "payouts_fields": "payments_out_table",
                   "packin_fields": "",
                   "packout_fields": "",
                   "invout_fields": "",
                   "invin_fields": "",

                   "customers_bal_fields": "",
                   "customers_fields": "",

                   }

    def __init__(self):
        super().__init__()

    def get_products_report(self, from_date=None, to_date=None):
        data_name = "products_table"
        from API_MS.ContMS.ContMSProdList import ContMSProdList
        data = ContMSProdList().get_prod_list_filtered_by_updated(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} prod report ready")
        self.save_data_2file(data_dict=data, file_name=data_name)
        return data


    def get_stockall_report(self, from_date=None, to_date=None):
        data_name = "stock_remains_table"
        from API_MS.ContMS.ContMSStockRemains import ContMSStockRemains
        data = ContMSStockRemains().get_stock_remains(to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data["stock"]["rows"]})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        self.save_data_2file(data_dict=data, file_name=data_name)
        return data

    def get_stockstore_report(self, from_date=None, to_date=None):
        data_name = "stock_bystore_table"
        from API_MS.ContMS.ContMSStockByStores import ContMSStockByStores
        data = ContMSStockByStores().get_stock_by_store(to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        self.save_data_2file(data_dict=data, file_name=data_name)
        return data

    def get_profit_by_product(self, from_date=None, to_date=None):
        data_name = "profit_byprod_table"
        from API_MS.ContMS.ContMSProfitProd import ContMSProfitProd
        data = ContMSProfitProd().get_profit_by_prod(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data["products"]["rows"]})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        self.save_data_2file(data_dict=data, file_name=data_name)
        return data

    def get_profit_by_customer(self, from_date=None, to_date=None):
        data_name = "profit_bycust_table"
        from API_MS.ContMS.ContMSProfitCust import ContMSProfitCust
        data = ContMSProfitCust().get_profit_by_cust(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data["customers"]["rows"]})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        self.save_data_2file(data_dict=data, file_name=data_name)
        return data

    def get_payments_in(self, from_date=None, to_date=None):
        data_name = "payments_in_table"
        from API_MS.ContMS.ContMSPayIn import ContMSPayIn
        data = ContMSPayIn().get_payin_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        self.save_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_payments_out(self, from_date=None, to_date=None):
        data_name = "payments_out_table"
        from API_MS.ContMS.ContMSPayOut import ContMSPayOut
        data = ContMSPayOut().get_payout_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        self.save_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def save_data_2file_json(self, data_dict, file_name):
        """ method save dict data to file in class ConnMSSaveFile"""
        from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
        try:
            ConnMSSaveJson().save_data_json_file(data_dict=data_dict, file_name=file_name)
        except Exception as e:
            print(e)


    def ms_main_requester(self, from_date=None, to_date=None):
        summary = dict()
        # requested_data = controller.get_products_report(from_date=from_date, to_date=to_date)
        # summary[requested_data.get("name")] = requested_data.get("data", [])
        # requested_data = controller.get_stockall_report(from_date=from_date, to_date=to_date)
        # summary[requested_data.get("name")] = requested_data.get("data", [])
        # requested_data = controller.get_stockstore_report(from_date=from_date, to_date=to_date)
        # summary[requested_data.get("name")] = requested_data.get("data", [])
        # requested_data = controller.get_profit_by_product(from_date=from_date, to_date=to_date)
        # summary[requested_data.get("name")] = requested_data.get("data", [])
        # requested_data = controller.get_profit_by_customer(from_date=from_date, to_date=to_date)
        # summary[requested_data.get("name")] = requested_data.get("data", [])
        # requested_data = controller.get_payments_in(from_date=from_date, to_date=to_date)
        # summary[requested_data.get("name")] = requested_data.get("data", [])
        requested_data = controller.get_payments_out(from_date=from_date, to_date=to_date)
        summary[requested_data.get("name")] = requested_data.get("data", [])

        self.save_data_2file_json(summary, "summary_tables")
        return summary


if __name__ == '__main__':
    controller = MSMain()
    data = controller.ms_main_requester(from_date="2023-05-01", to_date="2023-05-24")
    # data = controller.get_stockall_report(from_date="2023-05-01", to_date="2023-02-01")
    # data = controller.get_stockstore_report(from_date="2023-05-01", to_date="2023-02-01")
    print(data)
