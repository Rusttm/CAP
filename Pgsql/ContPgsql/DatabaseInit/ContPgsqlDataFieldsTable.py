from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
# from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
from Pgsql.ContPgsql.DatabaseInit.ContPgsqlReadFieldJson import ContPgsqlReadFieldJson
from Pgsql.ConnPgsql.ConnPgsqlDataGet import ConnPgsqlDataGet
from Pgsql.ConnPgsql.ConnPgsqlDataPut import ConnPgsqlDataPut


class ContPgsqlDataFieldsTable(ConnPgsqlTables, ContPgsqlReadFieldJson, ContPgsqlMainClass, ConnPgsqlDataGet, ConnPgsqlDataPut):
    """ connector for read fields tables from pgsql database"""
    fields_dict = None

    def __init__(self):
        super().__init__()
        self.make_local_dicts()

    def make_local_dicts(self):
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.fields_tables_list = ContPgsqlReadJsonTablesDict().get_field_tables_list()

    def fill_field_table_from_json(self, field_file_name=None, table_name=None):
        """ get data from field file and fill them"""
        self.fields_dict = self.get_fields_table_data_from_json(field_file_name=field_file_name)
        if not self.fields_dict:
            raise NotImplementedError(f"configuration json file {field_file_name} doesn't exist, please configure it")
        table_name = self.fields_dict.get("table", "unknown_table")
        if table_name:
            self.put_data_from_json(table_name=table_name, fields_dict=self.fields_dict)
            return True
        return False
    def put_data_from_json(self, table_name, fields_dict):
        """ takes data from json file and put it in sql table"""
        data = dict(fields_dict["data"])
        for key, data_dict in data.items():
            col_names_list = ["field_name"] + [f"field_{col_name}" for col_name in data_dict.keys()] + ["field_pg_type"]
            col_values_list = [key] + [str(value) for value in data_dict.values()]
            col_pg_type = self.types_mapper(data_dict.get("type"))
            col_values_list.append(col_pg_type)
            self.put_data_2table(table_name=table_name, col_names_list=col_names_list, col_values_list=col_values_list)

    def fill_all_field_tables(self):
        """ fill all field tables"""
        for table_name, data_dict in self.tables_dict.items():
            if data_dict.get('sql_upd', 0) != 1:
                try:
                    self.fields_tables_list.remove(data_dict.get('fields_table', None))
                except Exception as e:
                    print(e)
        for i, file_name in enumerate(self.fields_tables_list):
            # self.table_is_exist(table_name=)
            self.fill_field_table_from_json(field_file_name=file_name)
            print(f"filled table {i+1}({len(self.fields_tables_list)}) {file_name}")


if __name__ == '__main__':
    connector = ContPgsqlDataFieldsTable()
    connector.fill_all_field_tables()
    # connector.create_field_table_from_json(field_file_name='stockall_fields')
    # print(f"tables list {connector.get_tables_list()}")
    # print(f"try to create table from 'product_fields.json' result - {connector.create_table_from_json_field(file_name='product_fields.json')}")
    # print(connector.get_full_data(table_name='product_fields'))
    # print(connector.fill_data_from_json())
    # print(connector.delete_all_fields_tables())
