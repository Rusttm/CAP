from API_MS.MSMainClass import MSMainClass


class MSMain(MSMainClass):
    """ this class gather all reports together
    in one dict: {"products_table":[], "stock_remains_table":[]}"""
    tables_dict = {"products_table": {"fields_list": "product_fields", "function": "get_products_report"},
                   "stock_remains_table": {"fields_list": "stockall_fields", "function": "get_stockall_report"},
                   "stock_bystore_table": {"fields_list": "stockstore_fields", "function": "get_stockstore_report"},
                   "profit_byprod_table": {"fields_list": "profit_byprod_fields", "function": "get_profit_by_product"},
                   "profit_bycust_table": {"fields_list": "profit_bycust_fields", "function": "get_profit_by_customer"},
                   "payments_in_table": {"fields_list": "payins_fields", "function": "get_payments_in"},
                   "payments_out_table": {"fields_list": "payouts_fields", "function": "get_payments_out"},
                   "packlists_in_table": {"fields_list": "packin_fields", "function": "get_pack_lists_in"},
                   "packlists_out_table": {"fields_list": "packout_fields", "function": "get_pack_lists_out"},
                   "invoices_out_table": {"fields_list": "invout_fields", "function": "get_invoices_in"},
                   "invoices_in_table": {"fields_list": "invin_fields", "function": "get_invoices_out"},
                   "customers_bal_table": {"fields_list": "customers_bal_fields", "function": "get_customers_bal_report"},
                   "customers_table": {"fields_list": "customers_fields", "function": "get_customers_report"}
                   }

    def __init__(self):
        super().__init__()

    def get_products_report(self, from_date=None, to_date=None, to_file=False):
        data_name = "products_table"
        from API_MS.ContMS.ContMSProdList import ContMSProdList
        data = ContMSProdList().get_prod_list_filtered_by_updated(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_customers_report(self, from_date=None, to_date=None, to_file=False):
        data_name = "customers_table"
        from API_MS.ContMS.ContMSCustBal import ContMSCustBal
        data = ContMSCustBal().get_cust_bal(from_date=from_date, to_date=to_date, to_file=False)
        data = data.get("customers", [])
        data = dict({"name": data_name, "data": data.get("rows", [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_customers_bal_report(self, from_date=None, to_date=None, to_file=False):
        data_name = "customers_bal_table"
        from API_MS.ContMS.ContMSCustList import ContMSCustList
        data = ContMSCustList().get_custom_list_filtered_by_updated(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_stockall_report(self, from_date=None, to_date=None, to_file=False):
        data_name = "stock_remains_table"
        from API_MS.ContMS.ContMSStockRemains import ContMSStockRemains
        data = ContMSStockRemains().get_stock_remains(to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data["stock"]["rows"]})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_stockstore_report(self, from_date=None, to_date=None, to_file=False):
        data_name = "stock_bystore_table"
        from API_MS.ContMS.ContMSStockByStores import ContMSStockByStores
        data = ContMSStockByStores().get_stock_by_store(to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_profit_by_product(self, from_date=None, to_date=None, to_file=False):
        data_name = "profit_byprod_table"
        from API_MS.ContMS.ContMSProfitProd import ContMSProfitProd
        data = ContMSProfitProd().get_profit_by_prod(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data["products"]["rows"]})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_profit_by_customer(self, from_date=None, to_date=None, to_file=False):
        data_name = "profit_bycust_table"
        from API_MS.ContMS.ContMSProfitCust import ContMSProfitCust
        data = ContMSProfitCust().get_profit_by_cust(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data["customers"]["rows"]})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_payments_in(self, from_date=None, to_date=None, to_file=False):
        data_name = "payments_in_table"
        from API_MS.ContMS.ContMSPayIn import ContMSPayIn
        data = ContMSPayIn().get_payin_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_payments_out(self, from_date=None, to_date=None, to_file=False):
        data_name = "payments_out_table"
        from API_MS.ContMS.ContMSPayOut import ContMSPayOut
        data = ContMSPayOut().get_payout_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data":  data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_pack_lists_in(self, from_date=None, to_date=None, to_file=False):
        data_name = "packlists_in_table"
        from API_MS.ContMS.ContMSPackIn import ContMSPackIn
        data = ContMSPackIn().get_packin_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_pack_lists_out(self, from_date=None, to_date=None, to_file=False):
        data_name = "packlists_out_table"
        from API_MS.ContMS.ContMSPackOut import ContMSPackOut
        data = ContMSPackOut().get_packout_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_invoices_in(self, from_date=None, to_date=None, to_file=False):
        data_name = "invoices_in_table"
        from API_MS.ContMS.ContMSInvIn import ContMSInvIn
        data = ContMSInvIn().get_invin_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def get_invoices_out(self, from_date=None, to_date=None, to_file=False):
        data_name = "invoices_out_table"
        from API_MS.ContMS.ContMSInvOut import ContMSInvOut
        data = ContMSInvOut().get_invout_filtered_by_date(from_date=from_date, to_date=to_date, to_file=False)
        data = dict({"name": data_name, "data": data.get('rows', [])})
        self.logger.debug(f"{__class__.__name__} {data_name} report ready")
        if to_file:
            self.save_table_data_2file_json(data_dict=data, file_name=data_name)
        return data

    def save_table_data_2file_json(self, data_dict, file_name):
        """ method save dict data to file in class ConnMSSaveFile"""
        from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveJson
        try:
            ConnMSSaveJson().save_data_json_file(data_dict=data_dict, file_name=file_name, dir_name="data/tables")
            self.logger.debug(f"{__class__.__name__} file {file_name} saved")
        except Exception as e:
            print(e)

    def get_all_data_from_ms(self, from_date=None, to_date=None, to_file=False):
        """ request all data from MoiSklad """
        summary = dict()
        my_class = MSMain()
        for table_name, table_data in self.tables_dict.items():
            table_func = table_data.get("function", None)
            f = getattr(my_class, table_func)
            requested_data = f(from_date=from_date, to_date=to_date, to_file=to_file)
            summary[requested_data.get("name")] = requested_data.get("data", [])
            self.logger.debug(f"{__class__.__name__} data {table_name} was added to summary")
        if to_file:
            self.save_table_data_2file_json(summary, "summary_tables")
        self.logger.debug(f"{__class__.__name__} summary data from MoiSklad was formed")
        return summary


if __name__ == '__main__':
    controller = MSMain()
    # data = controller.get_all_data_from_ms(from_date="2023-05-01", to_date="2023-05-24")
    data = controller.get_all_data_from_ms()
    # data = controller.get_stockall_report(from_date="2023-05-01", to_date="2023-02-01")
    # data = controller.get_stockstore_report(from_date="2023-05-01", to_date="2023-02-01")
    # print(data)
