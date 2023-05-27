from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlData(ConnPgsqlMainClass):
    """returns data from tables"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()

    def get_full_data(self, table_name=None):
        """ select all from table"""
        req_line = f"SELECT * FROM {table_name}"
        if table_name:
            try:
                ans = self.send_get_request(req_line=req_line)
                return ans
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} error while request table {table_name}: {e}")
        else:
            self.logger.warning(f"{__class__.__name__} request not specified table_name={table_name}")
            self.logger.info(f"{__class__.__name__} please try request 'get_tables_list'")
        return None

    def get_cols_from_table(self, table_name=None, col_list=None):
        col_string = ', '.join(col_list)
        req_line = f"SELECT {col_string} FROM {table_name}"
        # req_line = f"SELECT field_name FROM {table_name}"
        # req_line = f"SELECT json_build_object('id', json_agg({table_name}.field_name)) FROM {table_name}"
        if table_name and col_list:
            try:
                ans = self.send_get_request(req_line=req_line)
                return ans
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} error while request cols table {table_name}: {e}")
        else:
            self.logger.warning(f"{__class__.__name__} request not specified table_name={table_name} or col_list={col_list}")
            self.logger.info(f"{__class__.__name__} please try request 'get_tables_list'")
        return None

    def get_value_cols_from_table(self, table_name=None, col_name=None, col_value=None, col_ans=None):
        """ request col_name='col_value'
        return vale of col_ans [('attributes', 'JSON[]')] """
        col_string = f"{col_name}, {col_ans}"
        req_line = f"SELECT {col_string} FROM {table_name} WHERE {col_name}='{col_value}'"
        # req_line = f"SELECT field_name FROM {table_name}"
        # req_line = f"SELECT json_build_object('id', json_agg({table_name}.field_name)) FROM {table_name}"
        if table_name and col_name and col_value and col_ans:
            try:
                ans = self.send_get_request(req_line=req_line)
                return ans
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} error while request cols table {table_name}: {e}")
        else:
            self.logger.warning(f"{__class__.__name__} request not specified table_name={table_name} or col_list={col_name}")
            self.logger.info(f"{__class__.__name__} please try request 'get_tables_list'")
        return None

    def put_data_2table(self, table_name: str, col_names_list: list, col_values_list: list):
        # column_string = ', '.join(col_names_list)
        col_values_string = self.values_in_request_handler(col_values_list, table_name)
        col_names_string = self.columns_in_request_handler(col_names_list, table_name)
        req_line = f"INSERT INTO {table_name}  {col_names_string} VALUES {col_values_string}"
        try:
            ans = self.send_get_request(req_line=req_line)
            return ans
        except Exception as e:
            # print(e)
            self.logger.error(f"{__class__.__name__} error while put data to table {table_name}: {e}")

    # def put_multiple_data_2table(self, table_name: str, col_names_list: list, col_values_lists: list):
    #     # column_string = ', '.join(col_names_list)
    #     col_multiple_values_string = self.values_list_in_request_handler(col_values_lists)
    #     col_names_string = self.columns_in_request_handler(table_name=table_name, col_names_list=col_names_list)
    #     req_line = f" INSERT INTO {table_name}  {col_names_string} VALUES {col_multiple_values_string}"
    #     try:
    #         ans = self.send_get_request(req_line=req_line)
    #         return ans
    #     except Exception as e:
    #         # print(e)
    #         self.logger.error(f"{__class__.__name__} error while put data to table {table_name}: {e}")

    def columns_in_request_handler(self, col_names_list, table_name=None):
        result_string = '( '
        for i, elem in enumerate(col_names_list):
            if elem == 'group':
                elem = 'group_ms'
            result_string += f'{elem}'
            if i < len(col_names_list) - 1:
                result_string += ", "

        result_string += ' )'
        result_string = result_string.replace("\\", "")
        return result_string

    def values_in_request_handler(self, col_values_list, table_name=None):
        """ add '{}' for json and
        return corrected list []"""
        temp_array = list()
        for elem in col_values_list:
            if elem == 'group':
                elem = 'group_ms'
            # null -> None -> null
            elif elem is None:
                elem = "null"
            temp_array.append(elem)
        result_string = str(tuple(temp_array))
        result_string = result_string.replace("\\'", "'")
        result_string = result_string.replace("json[]'", "json[]")
        result_string = result_string.replace("'array", "array")
        return result_string

    # def values_list_in_request_handler(self, col_values_lists):
    #     result_string = ""
    #     for i, values_list in enumerate(col_values_lists):
    #         result_string += self.values_in_request_handler(values_list)
    #         if i < len(col_values_lists) - 1:
    #             result_string += ", "
    #     return result_string



if __name__ == '__main__':
    connector = ConnPgsqlData()
    # data_from_table = connector.get_cols_from_table(table_name='product_fields', col_list=['id', 'field_name', 'field_pg_type'])
    # data_from_table = connector.get_value_cols_from_table(table_name='product_fields',
    #                                                       col_name='field_name',
    #                                                       col_value='attributes',
    #                                                       col_ans='field_pg_type')
    data_from_table = connector.get_full_data(table_name='product_fields')
    # print(f"try to get data from table 'test' {connector.get_full_data(table_name='product_fields')}")
    print(f"try to get info from table 'product_fields' {data_from_table}")
