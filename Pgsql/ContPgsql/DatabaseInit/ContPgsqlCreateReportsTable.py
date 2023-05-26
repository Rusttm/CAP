import time

from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from API_MS.MSMain import MSMain
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
# from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict


class ContPgsqlCreateReportsTable(ContPgsqlMainClass, MSMain, ConnPgsqlTables, ConnPgsqlData, ContPgsqlReadJsonTablesDict):
    """ class for creation report tables from fields tables"""
    ms_reports = None
    unique_columns = ['id', 'fields_name']
    tables_dict = None

    def __init__(self):
        super().__init__()
        # get all MS requests from MSMain class
        self.ms_reports = MSMain()
        self.tables_dict = self.get_tables_dict()

    def create_new_report_table(self, table_name=None):
        self.create_table_with_id(table_name=table_name)

    def add_col_2report_table(self, table_name=None, col_name=None, col_type=None):
        if col_name in self.unique_columns:
            self.create_unique_col_in_table(table_name=table_name, col_name=col_name)
        else:
            self.create_col_in_table(table_name=table_name, col_name=col_name, col_type=col_type)

    def get_full_info_fields_table(self, field_table_name=None):
        # field_table = dict(self.tables_dict).get(table_name)['fields_table']
        # print(controller.get_full_info_fields_table(table_name=field_table_name))
        field_table_data = self.get_full_data(table_name=field_table_name)
        return field_table_data

    def get_pgtype_info_fields_table(self, field_table_name=None):
        # field_table = dict(self.tables_dict).get(table_name)['fields_table']
        # print(controller.get_full_info_fields_table(table_name=field_table_name))
        # field_table_data = self.get_full_data(table_name=field_table_name)
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_cols_from_table(table_name=field_table_name, col_list=['field_name', 'field_pg_type'])
        # print(table_data)
        return dict(table_data)


    def get_pgtype_from_fields_table(self, field_table_name, col_value):
        """ return tuple field name and pg type('attributes', 'JSON[]')"""
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_value_cols_from_table(table_name=field_table_name,
                                                         col_name='field_name',
                                                         col_value=col_value,
                                                         col_ans='field_pg_type')
        try:
            result_tuple = table_data[0]
        except IndexError as e:
            result_tuple = (f"{col_value}", "TEXT")
            print(f"cant find field_pg_type for {col_value} in table {field_table_name}")
        except TypeError as e:
            result_tuple = (f"{col_value}", "TEXT")
            print(f"cant find field_pg_type for {col_value} in table {field_table_name}")
        return result_tuple

    def create_all_report_tables_by_schema(self):
        """ just create tables """
        for table_name, data_dict in self.tables_dict.items():
            field_table_name = data_dict.get('fields_table', None)
            self.create_new_report_table(table_name=table_name)
            data_fields = self.get_cols_from_table(table_name=field_table_name,
                                                   col_list=['field_name', 'field_pg_type'])
            for col_name, col_type in data_fields:
                self.create_col_in_table(table_name=table_name, col_name=col_name, col_type=col_type)
            print(f"table: {table_name} created")

    def fill_report_tables(self, from_date=None, to_date=None):
        from API_MS.MSMain import MSMain
        ms_connector = MSMain()
        for table_name, data_dict in self.tables_dict.items():
            if data_dict.get('sql', None) == 0:
                continue
            table_data_function = data_dict.get('function', None)
            request_func = getattr(ms_connector, table_data_function)
            req_data = request_func(from_date=from_date, to_date=to_date)
            data_list = req_data.get('data', [])
            field_table = data_dict.get('fields_table')
            fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
            gen_start = end = time.time()
            print(f"start :{time.ctime()} download in table: {table_name} positions: {len(data_list)}")
            for i, data_string in enumerate(data_list):
                col_names_list, col_values_list = self.col_values_list_handler(table_name=table_name,
                                                                               data_string=data_string,
                                                                               fields_dict=fields_dict)
                start = time.time()
                self.put_data_2table(table_name=table_name, col_names_list=col_names_list, col_values_list=col_values_list)
                end = time.time()
                print(f"send to table {table_name} position No:{i}({len(data_list)}) in:{round(end - start, 2)}sec")
            print(f"table: {table_name} downloded in {round(end - gen_start, 2)}sec")

    def fill_report_tables_multiple(self, from_date=None, to_date=None):
        """ !!!doesnt work cause lenth of data lists is different"""
        from API_MS.MSMain import MSMain
        ms_connector = MSMain()
        time_last = time.ctime()
        for table_name, data_dict in self.tables_dict.items():
            table_data_function = data_dict.get('function', None)
            request_func = getattr(ms_connector, table_data_function)
            req_data = request_func(from_date=from_date, to_date=to_date)
            data_list = req_data.get('data', [])
            print(f"количество позиций в таблице {table_name}: {len(data_list)}")
            col_names_list, col_values_lists = self.col_data_list_handler(table_name=table_name, data_list=data_list)
            self.put_multiple_data_2table(table_name=table_name,
                                          col_names_list=col_names_list,
                                          col_values_lists=col_values_lists)

    def col_values_list_handler(self, data_string, table_name, fields_dict=None):
        """ add '' for json and cast array[]::json[] to list
        return corrected """
        col_names_list = []
        col_values_list = []
        if fields_dict is None:
            field_table = self.tables_dict.get(table_name)['fields_table']
            fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
        for col_name, col_value in dict(data_string).items():
            if col_name == "group":
                col_name = "group_ms"
            col_names_list.append(col_name)
            # field_table = dict(self.tables_dict).get(table_name)['fields_table']
            col_type = fields_dict.get(col_name, 'TEXT')
            if type(col_value) == str:
                col_value = f'{col_value}'
            elif col_type == "JSON":
                col_value = str(col_value).replace("'", '"')
                # col_value = f"'{col_value}'"
            elif col_type == "JSON[]":
                new_json_array = []
                for json_elem in col_value:
                    json_elem = str(json_elem).replace("'", '"')
                    new_json_array.append(json_elem)
                col_value = 'array' + f'{new_json_array}' + '::json[]'
            col_values_list.append(col_value)

        return col_names_list, col_values_list

    def col_data_list_handler(self, data_list, table_name):
        """ from datalist of positions return list_list of values"""
        col_names_list = list(dict(data_list[0]).keys())
        col_values_list_list = []
        field_table = self.tables_dict.get(table_name)['fields_table']
        fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
        for i, pos_dict_list in enumerate(data_list):
            # col_values_list = list(dict(pos_dict_list).values())
            _, col_values_list_handled = self.col_values_list_handler(data_string=pos_dict_list,
                                                                      table_name=table_name,
                                                                      fields_dict=fields_dict)
            col_values_list_list.append(col_values_list_handled)
            print(f"handled {i} data string")
        return col_names_list, col_values_list_list



if __name__ == '__main__':
    controller = ContPgsqlCreateReportsTable()
    # controller.create_all_report_tables_by_schema()
    controller.fill_report_tables()
    # controller.fill_report_tables_multiple()

    # # controller.print_table_dict()
    # print(controller.get_full_info_fields_table(table_name='product_fields'))
    # req_data = controller.get_pgtype_from_fields_table(table_name='product_fields', col_value='attributes')
    # print(req_data)
