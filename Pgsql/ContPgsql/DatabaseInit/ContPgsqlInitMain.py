from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
import time

class ContPgsqlInitMain(ContPgsqlMainClass):
    def __init__(self):
        super().__init__()

    def initial_create_fields_tables(self):
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlCreateFieldsTable import ContPgsqlCreateFieldsTable
        result = ContPgsqlCreateFieldsTable().create_all_field_tables()
        return result

    def initial_create_report_tables(self):
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlCreateReportsTable import ContPgsqlCreateReportsTable
        result = ContPgsqlCreateReportsTable().create_all_report_tables_by_schema()
        print(f" report tables created!")
        return result

    def initial_fill_report_tables(self):
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlDataReportsTable import ContPgsqlDataReportsTable
        result = ContPgsqlDataReportsTable().fill_report_tables()
        print(f" report tables filled!")
        return result
    def initial_base_main(self):
        start = time.time()
        print(f"start db initialize at {time.ctime(start)}")
        fields_result = self.initial_create_fields_tables()
        now1 = time.time()
        print(f" fields tables created and filled in {round(now1 - start, 2)}sec")
        tables_result = self.initial_create_report_tables()
        now2 = time.time()
        print(f" report tables created in {round(now2 - now1, 2)}sec")
        tables_fill_result = self.initial_fill_report_tables()
        now3 = time.time()
        print(f" report tables filled in {round(now3 - now2, 2)}sec")
        end = time.time()
        print(f" database initiated in {round(end - start, 2)}sec")
        return {"fields_result": fields_result, "tables_result": tables_result, "tables_fill_result": tables_fill_result}


if __name__ == '__main__':
    controller = ContPgsqlInitMain()
    print(controller.initial_base_main())
