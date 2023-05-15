from API_MS.ContMS.ContMSMainClass import ContMSMainClass


import os
import json
import pathlib


class ContMSStores(ContMSMainClass):
    """ controller for MoiSklad stock remains by product"""
    connector = None
    file_name = "stores_dict.json"
    """ stores_dict.json - default file name for stores dict"""
    sum_file_name = "stores_sum.json"
    """ stores_sum.json - default file name for stores with summary num"""

    def __init__(self):
        super().__init__()
        # self.connector = ConnMSStockRemains()
        self.logger.debug(f"module {__class__.__name__} started")

    def get_stores_dict(self, to_file=False):
        """ return stores data as dictionary {store_name:0}"""
        from API_MS.ConnMS.ConnMSStores import ConnMSStores
        stores_dict = dict()
        stores = ConnMSStores().get_stores(to_file=to_file)
        if stores:
            for store in stores['rows']:
                # stores_dict[store['name']] = store['meta']['href']
                stores_dict[store['name']] = 0
        # if to_file:
        #     ConnMSSaveFile().save_data_json_file(data_dict=stores, file_name=self.file_name)
        return stores_dict

    def stores_sum(self, to_date=None, to_file=False):
        """ return dict {store:sum}"""
        from API_MS.ConnMS.ConnMSStockRemains import ConnMSStockRemains
        from API_MS.ConnMS.ConnMSStockByStore import ConnMSStockByStore
        # stock_remains = self.get_stock_remains(to_date=to_date)
        stock_remains = ConnMSStockRemains().get_stock_remains(to_date=to_date, to_file=to_file)
        # self.write_to_file(data_dict=stock_remains, file_name=self.file_name)
        stock_by_stores = ConnMSStockByStore().get_stock_by_store(to_date=to_date, to_file=to_file)
        stock_stores = self.get_stores_dict()
        stock_stores_sum = dict({"sum": 0, "stores": stock_stores})
        prod_href_dict = dict()  # {href:{name:name, price:price, quantity:quantity}}
        # collect remains to dict
        if stock_remains:
            for prod in stock_remains['stock']['rows']:
                prod_dict_temp = dict()
                prod_dict_temp['name'] = prod['name']
                prod_dict_temp['price'] = prod['price']
                prod_dict_temp['quantity'] = prod['quantity']
                prod_href_dict[prod['meta']['href']] = prod_dict_temp

        if stock_by_stores:
            for prod in stock_by_stores['rows']:
                prod_href = prod['meta']['href']
                prod_cost = 0
                # stores_sum = 0
                for prod_store in prod['stockByStore']:
                    try:
                        prod_cost = prod_href_dict[prod_href]['price'] / 100
                    except Exception as e:
                        print(e)
                    store_name = prod_store['name']
                    store_quantity = prod_store['stock']
                    stock_stores_sum["stores"][store_name] = stock_stores_sum["stores"].get(store_name, 0) + round(store_quantity * prod_cost, 2)
                    stock_stores_sum["sum"] += round(store_quantity * prod_cost, 2)
        if to_file:
            from API_MS.ConnMS.ConnMSSaveJson import ConnMSSaveFile
            ConnMSSaveFile().save_data_json_file(data_dict=stock_stores_sum, file_name=self.sum_file_name)
        return stock_stores_sum


if __name__ == '__main__':
    controller = ContMSStores()
    stores = controller.stores_sum(to_file=True)
    print(stores)
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
