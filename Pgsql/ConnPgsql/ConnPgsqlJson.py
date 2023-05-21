from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass
import json
import os


class ConnPgsqlJson(ConnPgsqlMainClass):
    """ convert fields from json file to dict"""
    dir_name = "data"

    def __init__(self):
        super().__init__()

    def get_fields_from_json(self, file_name=None):
        """ takes data from json files in dir ../data"""
        try:
            up_up_dir = os.path.dirname(os.path.dirname(__file__))
            json_file = os.path.join(up_up_dir, self.dir_name, file_name)
            with open(json_file, 'r') as jf:
                data = json.load(jf)
            return data
        except FileNotFoundError as e:
            self.logger.debug(f"File not found error json file: {e}")
            return False

    def get_json_files_list(self):
        """ gets files .json in ../data"""
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        files_list = os.listdir(os.path.join(up_up_dir, self.dir_name))
        json_files_list = [file for file in files_list if file.endswith(".json")]
        return json_files_list

    def get_all_dicts_in_dir(self):
        """ """
        json_files_list = self.get_json_files_list()
        result = list()
        for file in json_files_list:
            result.append(self.get_fields_from_json(file_name=file))
        return result

if __name__ == '__main__':
    connector = ConnPgsqlJson()
    ans = connector.get_fields_from_json("product_fields.json")
    # ans = connector.send_set_request("CREATE TABLE testtable (i integer);")
    print(ans)
    ans = connector.get_json_files_list()
    print(ans)
    ans = connector.get_all_dicts_in_dir()
    print(ans)
