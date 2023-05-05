from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSBalance import ConnMSBalance


class ContMSBalance(ContMSMainClass, ConnMSBalance):
    """ controller for MoiSklad balance
    get info from configfile and request information
    from ConnMSBalance connector
    return sum of accounts balance
    and return {dictionary account:bal}"""
    connector = None

    def __init__(self):
        super().__init__()
        self.logger.debug("module ContMSBalance started")


if __name__ == '__main__':
    controller = ContMSBalance()
    balance_sum = controller.get_sum()
    print(balance_sum)
    balance_acc = controller.get_accounts_bal()
    print(balance_acc)
