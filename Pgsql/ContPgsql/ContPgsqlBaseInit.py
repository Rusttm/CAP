from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass


class ContPgsqlBaseInit(ContPgsqlMainClass):

    def __init__(self):
        super().__init__()

    def create_table_from_json(self):
        pass


if __name__ == '__main__':
    connector = ContPgsqlBaseInit()
    print(f"create empty table {connector.create_table_from_json()}")
