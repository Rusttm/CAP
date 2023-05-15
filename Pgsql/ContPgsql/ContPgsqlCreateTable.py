from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.PgsqlSet.ConnPsqlCreateTable import ConnPsqlCreateTable


class ContPgsqlCreateTable(ContPgsqlMainClass, ConnPsqlCreateTable):
    """ connector for read tables from pgsql database"""

    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    connector = ConnPsqlCreateTable()
    # print(f"tables list {connector.get_tables_list()}")
    print(f"try to create table 'testtable' result - {connector.create_empty_table(table_name='testtable')}")
