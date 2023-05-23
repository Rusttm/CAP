from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson


class ContPgsqlCreateFieldsTable(ConnPgsqlTables, ConnPgsqlJson, ContPgsqlMainClass):
    """ connector for read tables from pgsql database"""

    def __init__(self):
        super().__init__()

    def create_empty_table_from_json_field(self, file_name=None):
        """ create tables for fields names and types"""
        fields_dict = dict(self.get_fields_from_json(file_name=file_name))
        table_name = fields_dict.get("table", "None")
        if table_name:
            result = self.create_table_with_id(table_name=table_name)
            # print(self.table_is_exist(table_name=table_name))
            for _, data_dict in fields_dict["data"].items():
                self.create_col_in_table(table_name=table_name, col_name="field_name", col_type="VARCHAR(255)")
                for name_col, _ in data_dict.items():
                    self.create_col_in_table(table_name=table_name, col_name=name_col, col_type="VARCHAR(255)")
                break
            return result
        return False

    def fill_data_from_json(self):
        pass



if __name__ == '__main__':
    connector = ContPgsqlCreateFieldsTable()
    # print(f"tables list {connector.get_tables_list()}")
    print(f"try to create table from 'product_fields.json' result - {connector.create_empty_table_from_json_field(file_name='product_fields.json')}")
