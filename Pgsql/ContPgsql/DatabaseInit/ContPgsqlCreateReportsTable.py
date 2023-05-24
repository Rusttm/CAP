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


if __name__ == '__main__':
    controller = ContPgsqlCreateReportsTable()
    controller.print_table_dict()