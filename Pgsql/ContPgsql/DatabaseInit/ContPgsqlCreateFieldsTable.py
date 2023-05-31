from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
# from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
# from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
from Pgsql.ContPgsql.DatabaseInit.ContPgsqlReadFieldJson import ContPgsqlReadFieldJson
from Pgsql.ConnPgsql.ConnPgsqlDataGet import ConnPgsqlDataGet
from Pgsql.ConnPgsql.ConnPgsqlDataPut import ConnPgsqlDataPut


class ContPgsqlCreateFieldsTable(ConnPgsqlTables, ContPgsqlReadFieldJson, ContPgsqlMainClass, ConnPgsqlDataGet, ConnPgsqlDataPut):
    """ connector for read fields tables from pgsql database"""
    fields_dict = None

    def __init__(self):
        super().__init__()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()
        self.fields_tables_list = ContPgsqlReadJsonTablesDict().get_field_tables_list()

    def create_field_table_from_json(self, field_file_name=None, table_name=None):
        """ get data from field file create tables for fields names and types and fulfillment them"""
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlReadFieldJson import ContPgsqlReadFieldJson
        self.fields_dict = ContPgsqlReadFieldJson().get_fields_table_data_from_json(field_file_name=field_file_name)
        if not self.fields_dict:
            raise NotImplementedError(f"configuration json file {field_file_name} doesn't exist, please configure it")
        table_name = self.fields_dict.get("table", "unknown_table")
        if table_name:
            result = self.create_table_with_id(table_name=table_name)
            # print(self.table_is_exist(table_name=table_name))
            self.add_columns_2table_from_json(table_name=table_name, fields_dict=self.fields_dict)
            # fill the field table
            # this class only create fields tables
            # self.put_data_from_json(table_name=table_name, fields_dict=self.fields_dict)
            return result
        return False

    def add_columns_2table_from_json(self, table_name, fields_dict):
        for _, data_dict in fields_dict["data"].items():
            self.create_col_in_table(table_name=table_name, col_name="field_name", col_type="VARCHAR(255)")
            self.mark_unique_col_in_table(table_name=table_name, col_name="field_name")
            # create column with datatypes of Postgresql
            self.create_col_in_table(table_name=table_name, col_name=f"field_pg_type", col_type="VARCHAR(255)")
            for name_col, _ in data_dict.items():
                self.create_col_in_table(table_name=table_name, col_name=f"field_{name_col}", col_type="VARCHAR(255)")
            break

    def create_all_field_tables(self):
        """ create all field tables and fulfillment them"""
        for table_name, data_dict in self.tables_dict.items():
            # create tables only with sql==1 in tables_dict
            # if data_dict.get('sql_upd', 0) != 1 or table_name in tables_in_db:
            if data_dict.get('sql_crt', 0) != 1:
                try:
                    self.fields_tables_list.remove(data_dict.get('fields_table', None))
                except Exception as e:
                    print(e)
        for i, file_name in enumerate(self.fields_tables_list):
            # self.table_is_exist(table_name=)
            self.create_field_table_from_json(field_file_name=file_name)
            print(f"created table {i+1}({len(self.fields_tables_list)}) {file_name}")

    def delete_all_fields_tables(self):
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        tables_dict_conn = ContPgsqlReadJsonTablesDict()
        fields_tables_list = tables_dict_conn.get_field_tables_list()
        for file_name in fields_tables_list:
            self.delete_table(table_name=file_name)
            print(f"deleted table {file_name}")


if __name__ == '__main__':
    connector = ContPgsqlCreateFieldsTable()
    connector.create_all_field_tables()
    # connector.create_field_table_from_json(field_file_name='stockall_fields')
    # print(f"tables list {connector.get_tables_list()}")
    # print(f"try to create table from 'product_fields.json' result - {connector.create_table_from_json_field(file_name='product_fields.json')}")
    # print(connector.get_full_data(table_name='product_fields'))
    # print(connector.fill_data_from_json())
    # print(connector.delete_all_fields_tables())
