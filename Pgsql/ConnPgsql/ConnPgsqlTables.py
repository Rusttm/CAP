from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlTables(ConnPgsqlMainClass):
    """ class for tables connection"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()

    def get_tables_list(self):
        req_line = "SELECT * FROM information_schema.tables WHERE table_schema = 'public'"
        ans = self.send_get_request(req_line=req_line)
        return ans

    def get_table_schema(self, table_name=None):
        req_line = f"SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name='{table_name}'"
        if table_name:
            try:
                ans = self.send_get_request(req_line=req_line)
                self.logger.warning(f"{__class__.__name__} request not specified table_name={table_name}")
                self.logger.info(f"{__class__.__name__} please try request 'get_tables_list'")
                return ans
            except Exception as e:
                self.logger.error(f"{__class__.__name__} error while request table {table_name}: {e}")
        return None

    def create_table_empty(self, table_name=None):
        """  create empty table  """
        ans = None
        if table_name:
            req_line = f"CREATE TABLE IF NOT EXISTS {table_name} ();"
            ans = self.send_set_request(req_line=req_line)
        return ans

    def create_table_with_id(self, table_name=None):
        """ creates table with id primary key"""
        ans = None
        if table_name:
            # req_line = f"CREATE TABLE IF NOT EXISTS {table_name} (id varchar(250) NOT NULL PRIMARY KEY);"
            req_line = f"CREATE TABLE IF NOT EXISTS {table_name} (position_id SERIAL PRIMARY KEY);"
            ans = self.send_set_request(req_line=req_line)
            print(ans.get('result', None))
        return ans.get('result', None)

    def create_col_in_table(self, table_name=None, col_name=None, col_type=None):
        if table_name and col_name and col_type and self.table_is_exist(table_name=table_name):
            column_type = self.types_mapper(type_ms=col_type)
            if column_type:
                req_line = f"ALTER TABLE IF EXISTS {table_name} ADD IF NOT EXISTS {col_name} {column_type}"
                ans = self.send_set_request(req_line=req_line)
                return ans
            else:
                self.logger.warning(f"{__class__.__name__} cant convert MoiSklad datatype: {col_type}")
        else:
            self.logger.warning(f"{__class__.__name__} receive wrong parameters")
        return False
    def create_unique_col_in_table(self, table_name=None, col_name=None):
        if table_name and col_name and self.table_is_exist(table_name=table_name):
            req_line = f"ALTER TABLE IF EXISTS {table_name} ADD UNIQUE ({col_name})"
            ans = self.send_set_request(req_line=req_line)
            return ans
        else:
            self.logger.warning(f"{__class__.__name__} receive wrong parameters")
        return False

    def table_is_exist(self, table_name=None):
        """ check is table exist in db? """
        if self.get_table_schema(table_name=table_name):
            return True
        return False

    def table_col_is_exist(self, table_name=None, col_name=None):
        """ check is col  exist in table? """
        if table_name and col_name and self.table_is_exist(table_name=table_name):
            req_line = f"SELECT {table_name}, {col_name}, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
            ans = self.send_set_request(req_line=req_line)
            return ans
        else:
            self.logger.warning(f"{__class__.__name__} receive wrong parameters")
        return False


    def delete_table(self, table_name=None):
        """  delete table 'table_name' """
        ans = None
        if table_name:
            req_line = f"DROP TABLE {table_name};"
            ans = self.send_set_request(req_line=req_line)
        return ans


if __name__ == '__main__':
    connector = ConnPgsqlTables()
    # print(f"tables list {connector.get_tables_list()}")
    # print(f"try to get table 'test' {connector.get_table_schema(table_name='test')}")
    print(f"create empty table {connector.create_table_with_id(table_name='test_empty_id')}")
    print(f"add col to empty table {connector.create_col_in_table(table_name='test_empty_id', col_name='test_col_1', col_type='String(255)')}")
    print(connector.get_table_schema(table_name='test_empty_id'))
    # print(f"create table {connector.create_table_with_id(table_name='test_empty_id')}")
    # print(connector.table_is_exist(table_name='test_empty_id'))
    # print(f"delete table 'test' {connector.delete_table(table_name='test_empty_id')}")
