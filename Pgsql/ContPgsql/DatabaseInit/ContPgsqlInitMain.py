from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass



class ContPgsqlInitMain(ContPgsqlMainClass, ContPgsqlCreateFieldsTable):
    def __init__(self):
        super().__init__()

    def initial_create_fields_tables(self):
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlCreateFieldsTable import ContPgsqlCreateFieldsTable
        result = ContPgsqlCreateFieldsTable().create_all_field_tables()
        print(f" fields tables downloaded!")
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
        fields_result = self.initial_create_fields_tables()
        tables_result = self.initial_create_report_tables()
        tables_fill_result = self.initial_fill_report_tables()
        return {"fields_result": fields_result, "tables_result": tables_result, "tables_fill_result": tables_fill_result}



if __name__ == '__main__':
    controller = ContPgsqlInitMain()
    print(controller.initial_base_main())
