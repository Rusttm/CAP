from Pgsql.PgsqlMainClass import PgsqlMainClass
import psycopg2


class ConnPgsqlDataMulty(PgsqlMainClass):
    """extend main class for multiply insertion
    initialise connection to pgsql database keys from config file"""
    pgsql_conn = None
    mapper = dict({
        "String(255)": "VARCHAR(255)",
        "Boolean": "BOOLEAN",
        "UUID": "UUID",
        "Array(Object)": "JSON[]",
        "Object": "JSON",
        "Meta": "JSON",
        "String(4096)": "TEXT",
        "Int": "INTEGER",
        "MetaArray": "JSON",  # not JSON[]
        "String": "TEXT",
        "Enum": "VARCHAR(255)",  # no enum in postgresql
        "DateTime": "TIMESTAMP",
        "Float": "REAL"
    })

    def __init__(self):
        super().__init__()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()

    def init_connection(self):
        from Pgsql.ConnPgsql.ConnPgsqlConfig import ConnPgsqlConfig
        try:
            conf = ConnPgsqlConfig().get_config()
            self.pgsql_conn = psycopg2.connect(
                host=conf['url'],
                port=conf['port'],
                database=conf['db_name'],
                user=conf['user'],
                password=conf['user_pass'])
            # self.cursor = self.pgsql_conn.cursor()
            self.logger.debug(f"{__class__.__name__} connector for PostgreSQL created")
        except Exception as e:
            # print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector for PostgreSQL! {e}")

    def fill_table_fast(self, table_name=None, data_dict=None):
        result_cols = []
        result_vals = []
        # data_dict = dict(data_dict)
        for dict_pos in data_dict:
            col_pack, val_pack = self.col_values_list_pre_handler(data_dict=dict_pos, table_name=table_name)
            col_string = self.columns_in_request_handler(col_names_list=col_pack)
            val_string = self.values_in_request_handler(col_values_list=val_pack)
            result_cols.append(col_string)
            result_vals.append(val_string)
        self.send_multi_insertion_request(table_name=table_name, col_string_list=result_cols, val_string_list=result_vals)

    def send_multi_insertion_request(self, table_name=None, col_string_list=None, val_string_list=None):
        self.init_connection()
        if self.pgsql_conn:
            try:
                with self.pgsql_conn as connection:
                    with connection.cursor() as my_cursor:
                        for i, col_string in enumerate(col_string_list):
                            val_string = val_string_list[i]
                            req_line = f"INSERT INTO {table_name}  {col_string} VALUES {val_string}"
                            my_cursor.execute(req_line)
                            self.logger.debug(f"{__class__.__name__} fetch cursor -'{req_line}'")
                            result_cursor = ['created!']
                            try:
                                result_cursor = my_cursor.connection.notices
                            except Exception as e:
                                print(e)
                            connection.commit()
                            self.logger.debug(f"{__class__.__name__} closed cursor -'{req_line}'")
                return dict({"result": result_cursor})
            except Exception as e:
                self.logger.error(f"{__class__.__name__} request error'{e}'")
            finally:
                self.pgsql_conn.close()
                self.logger.debug(f"{__class__.__name__} closed connector")
        else:
            self.logger.debug(f"{__class__.__name__} connector not valid == '{self.pgsql_conn}'")
        return None

    def get_pgtype_info_fields_table(self, field_table_name=None):
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_cols_from_table(table_name=field_table_name,
                                                   col_list=['field_name', 'field_pg_type'])
        return dict(table_data)

    def col_values_list_pre_handler(self, data_dict, table_name, fields_dict=None):
        """ add '' for json and cast array[]::json[] to list
        return corrected """
        col_names_list = []
        col_values_list = []
        if fields_dict is None:
            field_table = self.tables_dict.get(table_name)['fields_table']
            fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
        for col_name, col_value in dict(data_dict).items():
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

    def columns_in_request_handler(self, col_names_list):
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

    def values_in_request_handler(self, col_values_list):
        """ add '{}' for json and
        return corrected list []"""
        temp_array = list()
        for elem in col_values_list:
            if elem == 'group':
                elem = 'group_ms'
            temp_array.append(elem)
        result_string = str(tuple(temp_array))
        result_string = result_string.replace("\\'", "'")
        result_string = result_string.replace("json[]'", "json[]")
        result_string = result_string.replace("'array", "array")
        return result_string

if __name__ == '__main__':
    connector = ConnPgsqlDataMulty()
    print(connector.get_pgtype_info_fields_table(field_table_name='product_fields'))
    # ans = connector.send_get_request("SELECT version()")
    # ans = connector.send_set_request("CREATE TABLE testtable (i integer);")
    # print(ans)
