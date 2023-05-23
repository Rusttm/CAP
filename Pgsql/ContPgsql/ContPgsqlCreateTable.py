from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ARHIV.ConnPsqlCreateTable import ConnPsqlCreateTable
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson


class ContPgsqlCreateTable(ConnPsqlCreateTable, ConnPgsqlJson, ContPgsqlMainClass):
    """ connector for read tables from pgsql database"""

    def __init__(self):
        super().__init__()

    def create_empty_table_from_json(self, file_name=None):
        """ create tables for fields names and types"""
        fields_dict = self.get_fields_from_json(file_name=file_name)
        table_name = fields_dict['table']
        result = self.create_table_empty(table_name=table_name)
        from Pgsql.ContPgsql.ContPgsqlReadTable import ContPgsqlReadTable
        tables_reader = ContPgsqlReadTable()
        print(tables_reader.get_tables_list())
        return result


if __name__ == '__main__':
    connector = ContPgsqlCreateTable()
    # print(f"tables list {connector.get_tables_list()}")
    print(f"try to create table from 'product_fields.json' result - {connector.create_empty_table_from_json(file_name='product_fields.json')}")
