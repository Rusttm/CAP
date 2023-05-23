from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlData(ConnPgsqlMainClass):
    """returns data from tables"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()

    def get_full_data(self, table_name=None):
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

    def put_data_2table(self, table_name: str, col_names_list: list, col_values_list: list):
        column_list = ', '.join(col_names_list)
        req_line = f" INSERT INTO {table_name}  ({column_list}) VALUES {tuple(col_values_list)}"
        try:
            ans = self.send_get_request(req_line=req_line)
            return ans
        except Exception as e:
            # print(e)
            self.logger.error(f"{__class__.__name__} error while put data to table {table_name}: {e}")




if __name__ == '__main__':
    connector = ConnPgsqlData()
    print(f"try to get data from table 'test' {connector.get_full_data(table_name='product_fields')}")
