from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPsqlDelTable(ConnPgsqlMainClass):
    """connector for delete table"""

    def __init__(self):
        super().__init__()

    def delete_table(self, table_name=None):
        """  delete table 'table_name' """
        ans = None
        if table_name:
            req_line = f"DROP TABLE {table_name};"
            ans = self.send_set_request(req_line=req_line)
        return ans



if __name__ == '__main__':
    connector = ConnPsqlDelTable()
    print(f"delete table 'test' {connector.delete_table(table_name='test')}")
