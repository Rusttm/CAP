from Main.ContMain.ContCAPMainClass import ContCAPMainClass


import json

class ContCAPMS(ContCAPMainClass):
    """ MoiSklad API controller"""

    def __init__(self):
        super().__init__()

    def get_entity_bal_sum(self):
        from API_MS.ContMS.ContMSBalance import ContMSBalance
        controller = ContMSBalance()
        balance_sum = controller.get_sum()
        return balance_sum

    def get_entity_acc_bal(self):
        from API_MS.ContMS.ContMSBalance import ContMSBalance
        controller = ContMSBalance()
        balance_acc = controller.get_account_bal()
        return balance_acc

    def get_payouts(self):
        from API_MS.ContMS.ContMSPayOut import ContMSPayOut
        controller = ContMSPayOut()
        payouts = controller.get_payout_data()
        return payouts


if __name__ == '__main__':
    # check balances
    controller = ContCAPMS()
    balance_sum = controller.get_entity_bal_sum()
    print(balance_sum)
    # balance_acc = controller.get_entity_acc_bal()
    # print(balance_acc)

    # check payouts
    # payouts = controller.get_payouts()
    # FILE_PATH = "payouts.json"
    # with open(FILE_PATH, 'w') as ff:
    #     json.dump(payouts, ff, ensure_ascii=False)

    pass