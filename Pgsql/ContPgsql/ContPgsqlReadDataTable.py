from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData


class ContPgsqlReadDataTable(ContPgsqlMainClass, ConnPgsqlData):
    """ connector for read data from table"""

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ContPgsqlReadDataTable()
    # print(f"tables list {connector.get_tables_list()}")
    print(f"try to read from table 'testtable' result - {connector.get_full_data(table_name='product_fields')}")
