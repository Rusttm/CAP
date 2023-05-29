from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlDataHandler(ConnPgsqlMainClass):
    def __init__(self):
        super().__init__()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()

    def col_and_values_list_pre_handler(self, data_string, table_name, fields_dict=None):
        """ add '' for json and cast array[]::json[] and array[]::text[] to list
        return corrected """
        col_names_list = []
        col_values_list = []
        if fields_dict is None:
            field_table = self.tables_dict.get(table_name)['fields_table']
            fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
        for col_name, col_value in dict(data_string).items():
            if col_name == "group":
                col_name = "group_ms"
            if col_value is None:
                continue
            col_names_list.append(col_name)
            # field_table = dict(self.tables_dict).get(table_name)['fields_table']
            col_type = fields_dict.get(col_name, 'TEXT')
            if type(col_value) == str:
                col_value = f'{col_value}'
            elif col_type == "JSON":
                # "name": "ООО "АМЕТИСТ""
                for key, value in col_value.items():
                    if type(value) == str:
                        value = value.replace('"', "")
                    col_value[key] = value
                col_value = str(col_value).replace("'", '"')
                # col_value = f"'{col_value}'"
            elif col_type == "TEXT[]":
                new_string_array = []
                if type(col_value) == list:
                    for string_elem in col_value:
                        # string_elem = str(string_elem).replace('"', "")
                        new_string_array.append(string_elem)
                col_value = 'array' + f'{new_string_array}' + '::text[]'
            elif col_type == "JSON[]":
                new_json_array = []
                # single json[] not like list, but like json
                if type(col_value) == list:
                    for json_elem in col_value:
                        json_elem = str(json_elem).replace("'", '"')
                        new_json_array.append(json_elem)
                else:
                    json_elem = str(col_value).replace("'", '"')
                    new_json_array.append(json_elem)
                col_value = 'array' + f'{new_json_array}' + '::json[]'
            col_values_list.append(col_value)
        return col_names_list, col_values_list

    def get_pgtype_info_fields_table(self, field_table_name=None):
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_cols_from_table(table_name=field_table_name, col_list=['field_name', 'field_pg_type'])
        return dict(table_data)
