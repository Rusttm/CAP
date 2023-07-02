import time

from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from API_MS.MSMain import MSMain
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
# from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
from Pgsql.ConnPgsql.ConnPgsqlDataGet import ConnPgsqlDataGet
from Pgsql.ConnPgsql.ConnPgsqlDataPut import ConnPgsqlDataPut
from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict


class ContPgsqlCreateReportsTable(ContPgsqlMainClass, MSMain, ConnPgsqlTables, ConnPgsqlDataGet, ConnPgsqlDataPut):
    """ class for creation report tables from fields tables"""
    ms_reports = None
    unique_columns = ['id', 'fields_name']
    tables_dict = None

    def __init__(self):
        super().__init__()
        # get all MS requests from MSMain class
        self.ms_reports = MSMain()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()

    def create_new_report_table(self, table_name=None):
        self.create_table_with_id(table_name=table_name)

    def add_col_2report_table(self, table_name=None, col_name=None, col_type=None):
        table_dict = self.tables_dict.get(table_name)
        unique_col = table_dict.get("unique")
        # if col_name in self.unique_columns:
        if col_name == unique_col:
            self.create_col_in_table(table_name=table_name, col_name=col_name, col_type=col_type)
            self.mark_unique_col_in_table(table_name=table_name, col_name=col_name)
        else:
            self.create_col_in_table(table_name=table_name, col_name=col_name, col_type=col_type)

    def create_all_report_tables_by_schema(self):
        """ just create tables """
        tables_in_db = self.get_tables_list()
        for table_name, data_dict in self.tables_dict.items():
            if data_dict.get('sql_crt', None) != 1 or table_name in tables_in_db:
                continue
            field_table_name = data_dict.get('fields_table', None)
            self.create_new_report_table(table_name=table_name)
            data_fields = self.get_cols_from_table(table_name=field_table_name, col_list=['field_name', 'field_pg_type'])
            for col_name, col_type in data_fields:
                self.add_col_2report_table(table_name=table_name, col_name=col_name, col_type=col_type)
            print(f"table: {table_name} created")
        return True


if __name__ == '__main__':
    controller = ContPgsqlCreateReportsTable()
    controller.create_all_report_tables_by_schema()
    # controller.fill_report_tables()
    # controller.fill_report_tables_multiple()

    # # controller.print_table_dict()
    # print(controller.get_full_info_fields_table(table_name='product_fields'))
    # req_data = controller.get_pgtype_from_fields_table(table_name='product_fields', col_value='attributes')
    # print(req_data)
