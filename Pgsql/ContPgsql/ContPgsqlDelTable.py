from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ARHIV.ConnPsqlDelTable import ConnPsqlDelTable
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables


class ContPgsqlDelTable(ContPgsqlMainClass, ConnPsqlDelTable, ConnPgsqlTables):
    """ connector for delete table from pgsql database"""

    def __init__(self):
        super().__init__()

    def delete_all_tables_in_db(self):
        tables_list = self.get_tables_tuple_list()
        for tuple_line in tables_list:
            table_name = tuple_line[2]
            self.delete_table(table_name=table_name)
            print(f"table: {table_name} was deleted")


if __name__ == '__main__':
    connector = ContPgsqlDelTable()
    connector.delete_all_tables_in_db()
    # print(f"tables list {connector.get_tables_list()}")
    # print(f"try delete table 'testtable' result - {connector.delete_table(table_name='testtable')}")
