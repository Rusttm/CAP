from  Pgsql.PgsqlMainClass import PgsqlMainClass


class PgsqlMain(PgsqlMainClass):

    def __init__(self):
        super().__init__()
        self.make_fields_tables()

    def make_fields_tables(self):
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlCreateFieldsTable import ContPgsqlCreateFieldsTable
        controller = ContPgsqlCreateFieldsTable()
        controller.create_all_field_tables()
        # controller.delete_all_fields_tables()


if __name__ == '__main__':
    connector = PgsqlMain()