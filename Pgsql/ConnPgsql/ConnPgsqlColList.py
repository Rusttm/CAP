from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlColList(ConnPgsqlMainClass):

    def __init__(self):
        super().__init__()

    def get_col_list_table(self, table_name=None):
        """ return list of columns"""
        result_list = []
        if table_name:
            # req_line = f"SELECT * FROM {table_name} WHERE false"
            req_line = f"SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}'"
            ans = self.send_get_request(req_line=req_line)
            for col in ans:
                result_list.append(col[3])
        return result_list

    def count_col_table(self, table_name=None):
        """ return num of columns"""
        return len(self.get_col_list_table(table_name=table_name))


if __name__ == '__main__':
    connector = ConnPgsqlColList()
    print(connector.count_col_table(table_name='invin_fields'))