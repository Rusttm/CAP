from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPsqlMainClass


class ConnPsqlReadDataTables(ConnPsqlMainClass):
    """returns data from tables"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()

    def get_table_data(self, table_name=None):
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


if __name__ == '__main__':
    connector = ConnPsqlReadDataTables()
    print(f"try to get data from table 'test' {connector.get_table_data(table_name='test')}")
