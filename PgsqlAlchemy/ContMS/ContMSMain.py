from PgsqlAlchemy.PgsqlAlchemyMainClass import PgsqlAlchemyMainClass
import datetime


class ContMSMain(PgsqlAlchemyMainClass):
    def __init__(self):
        super().__init__()

    def get_customers_bal_report(self, from_date: datetime = None, to_date: datetime = None) -> list:
        """ return customer balance report"""
        from PgsqlAlchemy.ConnMS.ConnMSCustBal import ConnMSCustBal
        req_data = ConnMSCustBal().get_cust_bal_rows_list(from_date=from_date, to_date=to_date)
        return req_data


if __name__ == '__main__':
    connector = ContMSMain()
    start = datetime.datetime(2023, 7, 1, 0, 0, 0)
    end = datetime.datetime(2023, 7, 7, 0, 0, 0)
    print(connector.get_customers_bal_report(from_date=start, to_date=end))
