from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from API_MS.MSMain import MSMain
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData


class ContPgsqlCreateReportsTable(ContPgsqlMainClass, MSMain):
    """ class for creation report tables from fields tables"""
    ms_reports = None

    def __init__(self):
        super().__init__()
        self.ms_reports = MSMain()

    def print_table_dict(self):
        print(self.tables_dict)

    def get_full_info_fields_table(self, ):
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_full_data(table_name='fields_list')
        print(table_data)



if __name__ == '__main__':
    controller = ContPgsqlCreateReportsTable()
    # controller.print_table_dict()
    controller.get_full_info_fields_table()