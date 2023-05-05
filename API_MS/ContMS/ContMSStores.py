from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSStores import ConnMSStores
import os
import json
import pathlib

class ContMSStores(ContMSMainClass, ConnMSStores):
    """ controller for MoiSklad stock remains by product"""
    connector = None

    def __init__(self):
        super().__init__()
        # self.connector = ConnMSStockRemains()
        self.logger.debug("module ContMSStockRemains started")

    def get_stores_dict(self, to_file=False):
        """ return stores data as dictionary {store_name:href}"""
        stores_dict = dict()
        stores = self.get_stores(to_file=to_file)
        if stores:
            for store in stores['rows']:
                stores_dict[store['name']] = store['meta']['href']
        if to_file:
            file = os.path.dirname(os.path.dirname(__file__))
            DATA_FILE_PATH = os.path.join(file, "data", "stores_dict.json")
            if not os.path.exists(DATA_FILE_PATH):
                open(DATA_FILE_PATH, 'x')
            if os.path.exists(DATA_FILE_PATH):
                self.logger.debug(f"start write request to file {pathlib.PurePath(DATA_FILE_PATH).name}")
                with open(DATA_FILE_PATH, 'w') as ff:
                    json.dump(stores_dict, ff, ensure_ascii=False)
                self.logger.debug(f"request was wrote to file {pathlib.PurePath(DATA_FILE_PATH).name}")
            else:
                self.logger.error(f"file {DATA_FILE_PATH} doesnt exist")

        return stores_dict


if __name__ == '__main__':
    controller = ContMSStores()
    stores = controller.get_stores_dict(to_file=True)
    print(stores)
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
