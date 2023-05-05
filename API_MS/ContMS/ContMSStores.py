from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSStores import ConnMSStores
from API_MS.ConnMS.ConnMSStockByStore import ConnMSStockByStore
from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSStockRemains import ConnMSStockRemains
import os
import json
import pathlib

class ContMSStores(ContMSMainClass, ConnMSStores, ConnMSStockByStore, ConnMSStockRemains):
    """ controller for MoiSklad stock remains by product"""
    connector = None

    def __init__(self):
        super().__init__()
        # self.connector = ConnMSStockRemains()
        self.logger.debug("module ContMSStores started")

    def write_to_file(self, data_dict=None, file_name="stores_dict"):
        file = os.path.dirname(os.path.dirname(__file__))
        DATA_FILE_PATH = os.path.join(file, "data", f"{file_name}.json")
        if not os.path.exists(DATA_FILE_PATH):
            open(DATA_FILE_PATH, 'x')
        if os.path.exists(DATA_FILE_PATH):
            self.logger.debug(f"start write request to file {pathlib.PurePath(DATA_FILE_PATH).name}")
            with open(DATA_FILE_PATH, 'w') as ff:
                json.dump(data_dict, ff, ensure_ascii=False)
            self.logger.debug(f"request was wrote to file {pathlib.PurePath(DATA_FILE_PATH).name}")
        else:
            self.logger.error(f"file {DATA_FILE_PATH} doesnt exist")


    def get_stores_dict(self, to_file=False):
        """ return stores data as dictionary {store_name:0}"""
        stores_dict = dict()
        stores = self.get_stores(to_file=to_file)
        if stores:
            for store in stores['rows']:
                # stores_dict[store['name']] = store['meta']['href']
                stores_dict[store['name']] = 0
        if to_file:
            self.write_to_file(data_dict=stores, file_name="stores_dict")
        return stores_dict
    def stores_sum(self, to_date=None, to_file=False):
        """ return dict {store:sum}"""
        stock_remains = self.get_stock_remains(to_date=to_date)
        self.write_to_file(data_dict=stock_remains, file_name="unknown_remains")
        stock_by_stores = self.get_stock_by_store(to_date=to_date)
        stock_stores = self.get_stores_dict()
        prod_href_dict = dict() # {href:{name:name, cost:cost, quantity:quantity}}
        if stock_remains:
            for prod in stock_remains['rows']:
                prod_dict_temp = dict()
                prod_dict_temp['name'] = prod['name']
                prod_dict_temp['cost'] = prod['cost']
                prod_dict_temp['quantity'] = prod['quantity']
                prod_href_dict[prod['meta']['href']] = prod_dict_temp
        if stock_by_stores:
            for prod in stock_remains['rows']:
                prod_href = prod['meta']['href']
                for prod_store in prod['stockByStore']:
                    prod_cost = prod_href_dict[prod_href]['cost']
                    store_name = prod_store['name']
                    store_quantity = prod_store['stock']
                    stock_stores[store_name] = stock_stores.get(store_name, 0) + store_quantity * prod_cost
        if to_file:
            self.write_to_file(data_dict=stock_stores, file_name="stores_sum")
        return stock_stores




if __name__ == '__main__':
    controller = ContMSStores()
    stores = controller.get_stock_remains(to_file=True)
    print(stores)
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
