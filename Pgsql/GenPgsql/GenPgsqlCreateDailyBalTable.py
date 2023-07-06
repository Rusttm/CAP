from Pgsql.GenPgsql.GenPgsqlMainClass import GenPgsqlMainClass
import time


class GenPgsqlCreateDailyBalTable(GenPgsqlMainClass):
    def __init__(self):
        super().__init__()

    def create_daily_bal_table(self):
        inn_like_col_list = self.get_all_customers_inns()
        self.create_cols_from_inns_list(inn_like_col_list)


    def get_all_customers_inns(self):
        # return list of inns from 'customers_table'
        from Pgsql.GenPgsql.GenPgsqlDataGet import GenPgsqlDataGet
        data_connector = GenPgsqlDataGet()
        inn_tuples_list = data_connector.get_cols_from_table(table_name='customers_table', col_list=['inn'])
        inn_like_col_list = [f"inn_{t[0]}" for t in inn_tuples_list if t[0]]
        return inn_like_col_list

    def create_cols_from_inns_list(self, inn_like_col_list):
        table_name = 'customers_daily_bal'
        # create columns in 'customers_daily_bal'
        from Pgsql.GenPgsql.GenPgsqlTables import GenPgsqlTables
        table_connector = GenPgsqlTables()
        start_time = time.time()
        # create table
        table_connector.create_table_with_id(table_name=table_name)
        # create date col
        table_connector.create_col_in_table(table_name=table_name, col_name='bal_date', col_type='TIMESTAMP')
        # create inn columns in table 'daily_bal_customers'
        for col_name in inn_like_col_list:
            table_connector.create_col_in_table(table_name=table_name, col_name=col_name, col_type='REAL')
        end_time = time.time()
        print(f"({round(end_time - start_time, 2)}sec) created columns {self.get_cols_from_table(table_name=table_name)} ")

    def get_cols_from_table(self, table_name='customers_daily_bal'):
        from Pgsql.GenPgsql.GenPgsqlColList import GenPgsqlColList
        col_connector = GenPgsqlColList()
        return col_connector.get_col_list_table(table_name=table_name)




if __name__ == '__main__':
    generator = GenPgsqlCreateDailyBalTable()
    generator.create_daily_bal_table()
    # print(f"tables list {connector.get_tables_list()}")
    # print(f"try to get table 'test' {connector.get_table_schema(table_name='test')}")
    # print(f"create empty table {connector.create_table_with_id(table_name='test_empty_id')}")
    # print(f"add col to empty table {connector.create_col_in_table(table_name='test_empty_id', col_name='test_col_1', col_type='String(255)')}")
    # print(connector.get_table_schema(table_name='test_empty_id'))
    # print(generator.get_tables_tuple_list())
    # print(f"create table {connector.create_table_with_id(table_name='test_empty_id')}")
    # print(connector.table_is_exist(table_name='test_empty_id'))
    # print(f"delete table 'test' {connector.delete_table(table_name='test_empty_id')}")
