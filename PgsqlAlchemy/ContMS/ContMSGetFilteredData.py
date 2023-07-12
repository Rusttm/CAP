from PgsqlAlchemy.ContMS.ContMSMain import ContMSMain
from PgsqlAlchemy.ConnMS.ConnMSFilter import ConnMSFilter


class ContMSGetFilteredData(ContMSMain, ConnMSFilter):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    getter = ContMSGetFilteredData()
    print(getter.get_ms_request_with_date_filter(url_table_name='url_customers_bal_list'))
