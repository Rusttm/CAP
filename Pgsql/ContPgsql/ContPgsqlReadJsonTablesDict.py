from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ContPgsql.DatabaseInit.ContPgsqlReadFieldJson import ContPgsqlReadFieldJson


class ContPgsqlReadJsonTablesDict(ContPgsqlMainClass, ConnPgsqlJson):
    file_name = 'tables_dict'
    dir_name = 'config'

    def __init__(self):
        super().__init__()

    def get_tables_dict(self):
        return dict(self.get_data_from_json(file_name=self.file_name, dir_name=self.dir_name))

    def get_field_tables_list(self):
        tables_dict = self.get_tables_dict()
        field_tables_list = []
        for table_name, data_dict in tables_dict.items():
            field_tables_list.append(data_dict.get("fields_table", None))
        return field_tables_list

    def get_functions_tables_list(self):
        tables_dict = self.get_tables_dict()
        field_tables_list = []
        for table_name, data_dict in tables_dict.items():
            field_tables_list.append(data_dict.get("function", None))
        return field_tables_list


if __name__ == '__main__':
    connector = ContPgsqlReadJsonTablesDict()
    print(connector.get_tables_dict())
    print(connector.get_field_tables_list())
    # print(connector.get_field_tables_list())
    # print(connector.get_functions_tables_list())



