from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
from Pgsql.ContPgsql.DatabaseInit.ContPgsqlReadFieldJson import ContPgsqlReadFieldJson


class ContPgsqlCreateFieldsTable(ConnPgsqlTables, ContPgsqlReadFieldJson, ContPgsqlMainClass, ConnPgsqlData):
    """ connector for read fields tables from pgsql database"""
    # tables_list = ['product_fields',
    #                'payins_fields', 'payouts_fields',
    #                'packin_fields', 'packout_fields',
    #                'invout_fields', 'invin_fields',
    #                'stockall_fields', 'stockstore_fields',
    #                'customers_bal_fields', 'customers_fields',
    #                'profit_byprod_fields', 'profit_bycust_fields']
    fields_dict = None

    def __init__(self):
        super().__init__()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()

    def create_field_table_from_json(self, field_file_name=None, table_name=None):
        """ get data from field file create tables for fields names and types and fulfillment them"""
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlReadFieldJson import ContPgsqlReadFieldJson
        self.fields_dict = ContPgsqlReadFieldJson().get_fields_table_data_from_json(field_file_name=field_file_name)
        table_name = self.fields_dict.get("table", "None")
        if table_name:
            result = self.create_table_with_id(table_name=table_name)
            # print(self.table_is_exist(table_name=table_name))
            self.add_columns_2table_from_json(table_name=table_name, fields_dict=self.fields_dict)
            self.put_data_from_json(table_name=table_name, fields_dict=self.fields_dict)
            return result
        return False

    def add_columns_2table_from_json(self, table_name, fields_dict):
        for _, data_dict in fields_dict["data"].items():
            self.create_col_in_table(table_name=table_name, col_name="field_name", col_type="VARCHAR(255)")
            self.create_unique_col_in_table(table_name=table_name, col_name="field_name")
            for name_col, _ in data_dict.items():
                self.create_col_in_table(table_name=table_name, col_name=f"field_{name_col}", col_type="VARCHAR(255)")
                # create column with datatypes of Postgresql
                self.create_col_in_table(table_name=table_name, col_name=f"field_pg_type", col_type="VARCHAR(255)")
            break

    def put_data_from_json(self, table_name, fields_dict):
        """ takes data from json file and put it in sql table"""
        data = dict(fields_dict["data"])
        for key, data_dict in data.items():
            col_names_list = ["field_name"] + [f"field_{col_name}" for col_name in data_dict.keys()] + ["field_pg_type"]
            col_values_list = [key] + [str(value) for value in data_dict.values()]
            col_pg_type = self.types_mapper(data_dict.get("type"))
            col_values_list.append(col_pg_type)
            self.put_data_2table(table_name=table_name, col_names_list=col_names_list, col_values_list=col_values_list)

    def create_all_field_tables(self):
        """ create all field tables and fulfillment them"""
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        fields_tables_list = ContPgsqlReadJsonTablesDict().get_field_tables_list()
        for table_name, data_dict in self.tables_dict.items():
            if data_dict.get('sql', None) == 0:
                try:
                    fields_tables_list.remove(data_dict.get('fields_table', None))
                except Exception as e:
                    print(e)
        for i, file_name in enumerate(fields_tables_list):
            # self.table_is_exist(table_name=)
            self.create_field_table_from_json(field_file_name=file_name)
            print(f"created table {i}({len(fields_tables_list)}) {file_name}")

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
