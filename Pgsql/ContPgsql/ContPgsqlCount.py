from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlRowCount import ConnPgsqlRowCount
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
from Pgsql.ConnPgsql.ConnPgsqlColList import ConnPgsqlColList


class ContPgsqlCount(ContPgsqlMainClass, ConnPgsqlRowCount, ConnPgsqlTables, ConnPgsqlColList):

    def __init__(self):
        super().__init__()

    def get_db_info(self):
        """ return information about tables"""
        result_dict = dict()
        tables_list = self.get_tables_tuple_list()
        for table in tables_list:
            table_dict = dict()
            table_name = table[2]
            table_rows_num = self.count_rows_in_table(table_name=table_name)
            table_col_list = self.get_col_list_table(table_name=table_name)
            table_cols_num = self.count_col_table(table_name=table_name)
            # table_dict["col_list"] = table_col_list
            # table_dict["name"] = table_name
            table_dict["rows_num"] = table_rows_num
            table_dict["cols_num"] = table_cols_num
            result_dict[table_name] = table_dict
        return result_dict


if __name__ == '__main__':
    controller = ContPgsqlCount()
    # print(controller.count_rows_in_table(table_name='packlists_out_table'))
    print(controller.get_db_info())
