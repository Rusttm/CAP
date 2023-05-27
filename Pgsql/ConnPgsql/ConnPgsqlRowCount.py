from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlRowCount(ConnPgsqlMainClass):

    def __init__(self):
        super().__init__()

    def count_rows_in_table(self, table_name=None):
        if table_name:
            req_line = f"SELECT COUNT(*) FROM {table_name}"
            ans = self.send_get_request(req_line=req_line)
        return ans[0][0]




if __name__ == '__main__':
    connector = ConnPgsqlRowCount()
    print(connector.count_rows_in_table(table_name='packlists_out_table'))