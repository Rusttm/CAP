from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSCorr import ConnMSCorr

class ContMSCorrBal(ContMSMainClass, ConnMSCorr):
    """ controller for MoiSklad"""
    connector = None
    file_name = "corr_bal.json"
    """ file_name - default file name for stores dict"""
    sum_file_name = "corr_bal_sum.json"
    """ sum_file_name - default file name for stores with summary sum"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSCorrBal()
    groups = controller.get_corrections(to_file=True)
    print(groups)
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
