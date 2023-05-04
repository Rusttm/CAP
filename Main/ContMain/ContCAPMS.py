from Main.ContMain.ContCAPMainClass import ContCAPMainClass
from API_MS.ContMS.ContMSBalance import ContMSBalance

class ContCAPMS(ContCAPMainClass):
    """ MoiSklad API controller"""

    def __init__(self):
        super().__init__()

    def get_entity_bal_sum(self):
        controller = ContMSBalance()
        balance_sum = controller.get_sum()
        return balance_sum

    def get_entity_acc_bal(self):
        controller = ContMSBalance()
        balance_acc = controller.get_account_bal()
        return balance_acc


if __name__ == '__main__':
    controller = ContCAPMS()
    balance_sum = controller.get_entity_bal_sum()
    print(balance_sum)
    balance_acc = controller.get_entity_acc_bal()
    print(balance_acc)


