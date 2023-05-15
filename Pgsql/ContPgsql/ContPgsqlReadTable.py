from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.PgsqlGet.ConnPsqlReadTables import ConnPsqlReadTables


class ContPgsqlReadTable(ContPgsqlMainClass, ConnPsqlReadTables):
    """ connector for read tables from pgsql database"""

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ContPgsqlReadTable()
    print(f"tables list {connector.get_tables_list()}")
    print(f"try to get table 'test' result = {connector.get_table(table_name='test')}")
