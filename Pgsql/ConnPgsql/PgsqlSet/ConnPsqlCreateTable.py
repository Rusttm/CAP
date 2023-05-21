from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPsqlCreateTable(ConnPgsqlMainClass):
    """returns tables list"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()

    def create_empty_table(self, table_name=None):
        """  create table  """
        ans = None
        if table_name:
            req_line = f"CREATE TABLE IF NOT EXISTS {table_name} (id varchar(250) NOT NULL PRIMARY KEY);"
            ans = self.send_set_request(req_line=req_line)
        return ans["connection"].notices

    # def create_table(self, table_dict=None):
    #     """  create table from dict """
    #     table_dict = dict({'name': 'test_table',
    #                        'fields': {'username': 'varchar(45) NOT NULL',
    #                                   'password': 'varchar(45) NOT NULL',
    #                                   'enabled': "integer NOT NULL DEFAULT '1'",
    #                                   'PRIMARY KEY': 'username'}})
    #     ans = None
    #     if table_dict:
    #         req_line = f""" CREATE TABLE IF NOT EXISTS {table_dict['name']} (
    #         username varchar(45) NOT NULL,
    #         password varchar(450) NOT NULL,
    #         enabled integer NOT NULL DEFAULT '1',
    #         PRIMARY KEY ({table_dict['fields']['PRIMARY KEY']})
    #         )"""
    #         ans = self.send_set_request(req_line=req_line)
    #     return ans


if __name__ == '__main__':
    connector = ConnPsqlCreateTable()
    print(f"create empty table {connector.create_empty_table(table_name='test')}")
