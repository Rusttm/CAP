from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from API_MS.MSMain import MSMain
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData


class ContPgsqlCreateReportsTable(ContPgsqlMainClass, MSMain, ConnPgsqlTables, ConnPgsqlData):
    """ class for creation report tables from fields tables"""
    ms_reports = None

    def __init__(self):
        super().__init__()
        self.ms_reports = MSMain()

    def print_table_dict(self):
        print(self.tables_dict)

    def create_new_report_table(self, table_name=None):
        self.create_table_with_id(table_name=table_name)

    def add_col_2report_table(self, table_name=None, col_name=None, col_type=None):
        if col_name == "UUID":
            self.create_unique_col_in_table(table_name=table_name, col_name=col_name)
        else:
            self.create_col_in_table(table_name=table_name, col_name=col_name, col_type=col_type)

    def get_full_info_fields_table(self, table_name=None):
        table_data = self.get_full_data(table_name=table_name)
        return table_data

    def get_pgtype_from_fields_table(self, table_name, col_value):
        """ return tuple field name and pg type('attributes', 'JSON[]')"""
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_value_cols_from_table(table_name=table_name,
                                                         col_name='field_name',
                                                         col_value=col_value,
                                                         col_ans='field_pg_type')
        return table_data[0]

    def create_all_report_tables_by_schema(self):
        tables_dict = self.tables_dict
        for table_name, data_dict in tables_dict.items():
            field_table_name = data_dict.get('fields_table', None)
            self.create_new_report_table(table_name=table_name)
            data_fields = self.get_cols_from_table(table_name=field_table_name,
                                                   col_list=['field_name', 'field_pg_type'])
            for col_name, col_type in data_fields:
                self.create_col_in_table(table_name=table_name, col_name=col_name, col_type=col_type)

        # print(self.get_full_info_fields_table())


if __name__ == '__main__':
    controller = ContPgsqlCreateReportsTable()
    controller.create_all_report_tables_by_schema()
    # # controller.print_table_dict()
    # print(controller.get_full_info_fields_table(table_name='product_fields'))
    # req_data = controller.get_pgtype_from_fields_table(table_name='product_fields', col_value='attributes')
    # print(req_data)
