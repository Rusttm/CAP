#~/cap_env/bin/python
from Pgsql.ContPgsql.ContPgsqlUpdater import ContPgsqlUpdater

class PgsqlUpdaterAir(ContPgsqlUpdater):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = PgsqlUpdaterAir()
    print(f"tables update {connector.update_all_report_tables()}")
    # print(f"tables update {connector.get_last_update_date_from_service()}")
    # print(f"try to get table 'test' result = {connector.get_table(table_name='test')}")