from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlTables import ConnPgsqlTables
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData

class ContPgsqlCreateReportsTable(ContPgsqlMainClass):
    """ class for creation report tables from fields tables"""
    tables_dict = ['product_fields',
                   'payins_fields', 'payouts_fields',
                   'packin_fields', 'packout_fields',
                   'invout_fields', 'invin_fields',
                   'stockall_fields', 'stockstore_fields',
                   'customers_bal_fields', 'customers_fields',
                   'profit_byprod_fields', 'profit_bycust_fields']


    def __init__(self):
        super().__init__()


