from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ARHIV.ConnPsqlDelTable import ConnPsqlDelTable


class ContPgsqlDelTable(ContPgsqlMainClass, ConnPsqlDelTable):
    """ connector for delete table from pgsql database"""

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ContPgsqlDelTable()
    # print(f"tables list {connector.get_tables_list()}")
    print(f"try delete table 'testtable' result - {connector.delete_table(table_name='testtable')}")
