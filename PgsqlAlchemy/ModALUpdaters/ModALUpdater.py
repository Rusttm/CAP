from PgsqlAlchemy.ModALUpdaters.ModALUpdaterMainClass import ModALUpdaterMainClass
import time

class ModALUpdater(ModALUpdaterMainClass):
    def __init__(self):
        super().__init__()

    def update_customers_balance(self):
        from PgsqlAlchemy.ModALUpdaters.ModALUpdCustBal import ModALUpdCustBal
        res = ModALUpdCustBal().update_cust_bal()
        return res


if __name__ == '__main__':
    updater = ModALUpdater()
    # connector.logger.info("testing ModALFillCustBal")
    # print(f"logger file name: {connector.logger_name}")
    # print(connector.get_last_update_date_from_service("customers_bal_table"))
    # print(connector.get_data_for_insertion("customers_bal_model"))
    start = time.time()
    res = updater.update_customers_balance()
    print(f"function result: {res}")
    print(f"function time = {round(time.time() - start, 2)}sec")