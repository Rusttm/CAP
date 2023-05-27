from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
import time
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
from Pgsql.ConnPgsql.ConnPgsqlDataMulty import ConnPgsqlDataMulty


class ContPgsqlDataReportsTable(ContPgsqlMainClass, ConnPgsqlData, ConnPgsqlDataMulty):
    """class for fulfillment data tables"""

    def __init__(self):
        super().__init__()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()



    def fill_report_tables_fast(self, from_date=None, to_date=None):
        from API_MS.MSMain import MSMain
        ms_connector = MSMain()
        for table_name, data_dict in self.tables_dict.items():
            if data_dict.get('sql', None) == 0:
                continue
            table_data_function = data_dict.get('function', None)
            request_func = getattr(ms_connector, table_data_function)
            # req_data = request_func(from_date="2022-12-01", to_date="2022-12-03")
            req_data = request_func()
            data_list = req_data.get('data', [])
            # field_table = data_dict.get('fields_table')
            # fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
            gen_start = end = time.time()
            print(f"start :{time.ctime()} download in table: {table_name} positions: {len(data_list)}")
            self.fill_table_fast(table_name=table_name, data_dict=data_list)
            # for i, data_string in enumerate(data_list):
            #     col_names_list, col_values_list = self.col_values_list_handler(table_name=table_name,
            #                                                                    data_string=data_string,
            #                                                                    fields_dict=fields_dict)
            #     start = time.time()
            #
            #     self.put_data_2table(table_name=table_name, col_names_list=col_names_list,
            #                          col_values_list=col_values_list)
            #     end = time.time()
            #     print(f"send to table {table_name} position No:{i}({len(data_list)}) in:{round(end - start, 2)}sec")
            print(f"table: {table_name} downloded in {round(end - gen_start, 2)}sec")

    def fill_report_tables(self, from_date=None, to_date=None):
        from API_MS.MSMain import MSMain
        ms_connector = MSMain()
        for table_name, data_dict in self.tables_dict.items():
            if data_dict.get('sql', None) == 0:
                continue
            table_data_function = data_dict.get('function', None)
            request_func = getattr(ms_connector, table_data_function)
            # req_data = request_func(from_date="2022-12-01", to_date="2022-12-03")
            req_data = request_func()
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

    # def col_data_list_handler(self, data_list, table_name):
    #     """ from datalist of positions return list_list of values"""
    #     col_names_list = list(dict(data_list[0]).keys())
    #     col_values_list_list = []
    #     field_table = self.tables_dict.get(table_name)['fields_table']
    #     fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
    #     for i, pos_dict_list in enumerate(data_list):
    #         # col_values_list = list(dict(pos_dict_list).values())
    #         _, col_values_list_handled = self.col_values_list_handler(data_string=pos_dict_list,
    #                                                                   table_name=table_name,
    #                                                                   fields_dict=fields_dict)
    #         col_values_list_list.append(col_values_list_handled)
    #         print(f"handled {i} data string")
    #     return col_names_list, col_values_list_list

    def get_pgtype_info_fields_table(self, field_table_name=None):
        # from Pgsql.ContPgsql.DatabaseInit.ContPgsqlReadFieldJson import ContPgsqlReadFieldJson
        # connector = ContPgsqlReadFieldJson()
        # table_data = connector.get_fields_table_data_from_json(field_file_name=field_table_name)
        # print(table_data)
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_cols_from_table(table_name=field_table_name, col_list=['field_name', 'field_pg_type'])
        return dict(table_data)


if __name__ == '__main__':
    controller = ContPgsqlDataReportsTable()
    # print(controller.get_pgtype_info_fields_table(field_table_name='product_fields'))
    controller.fill_report_tables_fast()