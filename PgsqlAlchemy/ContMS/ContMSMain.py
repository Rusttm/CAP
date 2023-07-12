from PgsqlAlchemy.PgsqlAlchemyMainClass import PgsqlAlchemyMainClass
import datetime


class ContMSMain(PgsqlAlchemyMainClass):
    def __init__(self):
        super().__init__()



if __name__ == '__main__':
    connector = ContMSMain()
    # start = datetime.datetime(2023, 7, 1, 0, 0, 0)
    # end = datetime.datetime(2023, 7, 7, 0, 0, 0)
    # print(connector.get_customers_bal_report(from_date=start, to_date=end))
