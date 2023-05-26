from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
import os
import json


class ContPgsqlReadFieldJson(ContPgsqlMainClass, ConnPgsqlJson):

    def __init__(self):
        super().__init__()

    def get_fields_table_data_from_json(self, field_file_name=None):
        """ takes data from json files in dir ../data"""
        dir_name = "config"
        if field_file_name:
            file_name_type = field_file_name.split(".")[-1]
            if file_name_type != "json":
                field_file_name += ".json"
        try:
            up_up_up_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            json_file = os.path.join(up_up_up_dir, dir_name, field_file_name)
            with open(json_file, 'r') as jf:
                data = json.load(jf)
            return dict(data)
        except FileNotFoundError as e:
            self.logger.debug(f"File not found error json file: {e}")
            return False


if __name__ == '__main__':
    connector = ContPgsqlReadFieldJson()
    print(connector.get_fields_table_data_from_json('invin_fields.json'))
    # print(f"tables list {connector.get_tables_list()}")
    # print(f"try to read from table 'testtable' result - {connector.get_table_data(table_name='testtable')}")
