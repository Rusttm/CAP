from CAPMain.ContMain.ContCAPMainClass import ContCAPMainClass
import json
import logging

class ContCAPMS(ContCAPMainClass):
    """ MoiSklad API main controller"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ContCAPMS started")

    def get_entity_bal_sum(self):
        from API_MS.ContMS.ContMSBalance import ContMSBalance
        controller = ContMSBalance()
        balance_sum = controller.get_sum()
        return balance_sum

    def get_entity_acc_bal(self):
        from API_MS.ContMS.ContMSBalance import ContMSBalance
        controller = ContMSBalance()
        balance_acc = controller.get_accounts_bal()
        return balance_acc

    def get_payouts_filtered(self, from_date=None, to_date=None):
        from API_MS.ContMS.ContMSPayOut import ContMSPayOut
        controller = ContMSPayOut()
        payouts = controller.get_payout_filtered_by_date(from_date, to_date)
        return payouts

    def get_payin_filtered(self, from_date=None, to_date=None):
        # ContCAPMS.logger.info(f"MoiSklad ContCAPMS controller id{self.id} successfully started")
        from API_MS.ContMS.ContMSPayIn import ContMSPayIn
        controller = ContMSPayIn()
        payins = controller.get_payin_filtered_by_date(from_date, to_date)
        return payins

    def get_stock_remains(self, to_date=None):
        from API_MS.ContMS.ContMSStockRemains import ContMSStockRemains
        controller_ms = ContMSStockRemains()
        stock_remains = controller_ms.get_stock_remains(to_date=to_date)
        return stock_remains

    def get_stock_stores(self, to_date=None):
        from API_MS.ContMS.ContMSStores import ContMSStores
        controller_ms = ContMSStores()
        stock_stores = controller_ms.stores_sum(to_date=to_date)
        return stock_stores

if __name__ == '__main__':
    controller = ContCAPMS()
    # check balances
    # controller = ContCAPMS()
    # balance_sum = controller.get_entity_bal_sum()
    # print(balance_sum)
    # balance_acc = controller.get_entity_acc_bal()
    # print(balance_acc)

    # check payouts
    # payouts = controller.get_payouts_filtered()
    # FILE_PATH = "payouts.json"
    # with open(FILE_PATH, 'w') as ff:
    #     json.dump(payouts, ff, ensure_ascii=False)

    # check payins all
    # payins = controller.get_payin_filtered()
    # FILE_PATH = "../../API_MS/data/payins.json"
    # with open(FILE_PATH, 'w') as ff:
    #     json.dump(payins, ff, ensure_ascii=False)

    # check payins filtered
    # payins = controller.get_payin_filtered(from_date="2023-01-01", to_date="2023-02-01")
    # FILE_PATH = "../../API_MS/data/payins_fitered.json"
    # with open(FILE_PATH, 'w') as ff:
    #     json.dump(payins, ff, ensure_ascii=False)

    # check payins half filtered
    # payins = controller.get_payin_filtered(from_date="2023-01-01")
    # FILE_PATH = "/Users/johnlennon/RusttmGDrive/Python/CAP/API_MS/data/payins_half_fitered2.json"
    # with open(FILE_PATH, 'w') as ff:
    #     json.dump(payins, ff, ensure_ascii=False)

    # check stock remains
    stock_remains = controller.get_stock_remains(to_date="2023-01-01")
    print(f"{stock_remains['sum']=}")
    # FILE_PATH = "/Users/johnlennon/RusttmGDrive/Python/CAP/API_MS/data/stock_all.json"
    # with open(FILE_PATH, 'w') as ff:
    #     json.dump(stock_remains, ff, ensure_ascii=False)

    # check stock remains by stores
    stock_remains_stores = controller.get_stock_stores(to_date="2023-01-01")
    print(f"{stock_remains_stores['sum']=}")
