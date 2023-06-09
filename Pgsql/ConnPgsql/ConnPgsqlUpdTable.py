from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlUpdTable(ConnPgsqlMainClass):
    """connector for saving data to table"""

    def __init__(self):
        super().__init__()

    def save_data_2table(self, data=None, table_name=None):
        """  save data 'data' to table 'table_name' """
        ans = None
        if table_name:
            req_line = f"Insert INTO {table_name}(id) VALUES ({data});"
            ans = self.send_set_request(req_line=req_line)
        return ans



if __name__ == '__main__':
    connector = ConnPgsqlUpdTable()
    print(f"put data to table 'test' {connector.save_data_2table(table_name='test', data='7686979')}")
