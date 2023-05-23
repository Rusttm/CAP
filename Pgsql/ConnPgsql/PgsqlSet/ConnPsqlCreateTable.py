from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPsqlCreateTable(ConnPgsqlMainClass):
    """returns tables list"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()

    def table_is_exist(self, table_name=None):
        from Pgsql.ConnPgsql.PgsqlGet.ConnPsqlReadTables import ConnPsqlReadTables
        if ConnPsqlReadTables().get_table_schema(table_name=table_name):
            return True
        return False

    def create_table_empty(self, table_name=None):
        """  create empty table  """
        ans = None
        if table_name:
            req_line = f"CREATE TABLE IF NOT EXISTS {table_name} ();"
            ans = self.send_set_request(req_line=req_line)
        return ans

    def  create_table_with_id(self, table_name=None):
        """ creates table with id primary key"""
        ans = None
        if table_name:
            # req_line = f"CREATE TABLE IF NOT EXISTS {table_name} (id varchar(250) NOT NULL PRIMARY KEY);"
            req_line = f"CREATE TABLE IF NOT EXISTS {table_name} (id varchar(255) NOT NULL PRIMARY KEY);"
            ans = self.send_set_request(req_line=req_line)
        return ans


if __name__ == '__main__':
    connector = ConnPsqlCreateTable()
    # print(f"create empty table {connector.create_table_empty(table_name='test_empty')}")
    print(f"create table {connector.create_table_with_id(table_name='test_empty_id')}")
    print(connector.table_is_exist(table_name='test_empty_id'))
