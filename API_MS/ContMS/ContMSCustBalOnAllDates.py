from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSCustBalByInn import ConnMSCustBalByInn
import datetime

class ContMSCustBalOnAllDates(ContMSMainClass, ConnMSCustBalByInn):
    """ controller for MoiSklad customers balances list from date to today"""
    left_date = '2018-10-01 00:00:00.000'
    right_date = f"{datetime.datetime.now().strftime('%Y-%m-%d')} 24:00:00"


    def __init__(self):
        super().__init__()
        # self.connector = ConnMSStockRemains()
        self.logger.debug(f"module {__class__.__name__} started")

    def get_list_of_client_balances(self, from_date: str = None, to_date: str = None, client_inn: str = None) -> list:
        """ date var must be like '2023-07-6 23:59:00.000' """
        if not from_date:
            from_date = datetime.datetime.strptime(self.left_date, "%Y-%m-%d %H:%M:%S.%f")
        if not to_date:
            to_date = datetime.datetime.now()
        if from_date > to_date:
            from_date, to_date = to_date, from_date

        days_diff = (to_date - from_date).days
        for day_num in range(days_diff):
            pass

        print(days_diff)


        print(f"{from_date + datetime.timedelta(days=1)}/{to_date=}")



if __name__ == '__main__':
    controller = ContMSCustBalOnAllDates()
    groups = controller.get_list_of_client_balances(client_inn='5403362299')
    print(groups)
    # stock = controller.get_stock_remains(to_file=True)
    # print(stock)
