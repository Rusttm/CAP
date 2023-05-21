from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPsqlMainClass


class ConnPsqlReadTables(ConnPsqlMainClass):
    """returns tables list"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()

    def get_table(self, table_name=None):
        req_line = f"SELECT {table_name} FROM information_schema.tables WHERE table_schema = 'public'"
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
    def get_tables_list(self):
        req_line = """SELECT * FROM information_schema.tables WHERE table_schema = 'public'"""
        ans = self.send_get_request(req_line=req_line)
        return ans


if __name__ == '__main__':
    connector = ConnPsqlReadTables()
    print(f"tables list {connector.get_tables_list()}")
    print(f"try to get table 'test' {connector.get_table(table_name='test')}")
