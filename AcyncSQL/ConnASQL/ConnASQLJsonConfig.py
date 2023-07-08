from AcyncSQL.ConnASQL.ConnASQLJson import ConnASQLJson
from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass



class ConnASQLJsonConfig(ConnASQLJson):
    file_name = 'async_tables_config'
    dir_name = 'config'

    def __init__(self):
        super().__init__()

    def get_tables_config(self) -> dict:
        return dict(self.get_data_from_json(file_name=self.file_name, dir_name=self.dir_name))

    def get_field_tables_list(self):
        tables_dict = self.get_tables_config()
        field_tables_list = []
        for table_name, data_dict in tables_dict.items():
            field_tables_list.append(data_dict.get("fields_table", None))
        return field_tables_list



if __name__ == '__main__':
    connector = ConnASQLJsonConfig()
    print(connector.get_tables_config())




