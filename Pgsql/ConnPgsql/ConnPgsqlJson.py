from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass
import json
import os


class ConnPgsqlJson(ConnPgsqlMainClass):
    """ convert fields from json file to dict"""
    dir_name = "config"

    def __init__(self):
        super().__init__()

    def get_json_files_list(self):
        """ gets files .json in ../data"""
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        files_list = os.listdir(os.path.join(up_up_dir, self.dir_name))
        json_files_list = [file for file in files_list if file.endswith(".json")]
        return json_files_list

    def get_all_dicts_in_dir(self, dir_name=None):
        """ """
        if dir_name is not None:
            self.dir_name = dir_name
        json_files_list = self.get_json_files_list()
        result = list()
        for file_name in json_files_list:
            result.append(file_name)
        return result

    def get_data_from_json(self, file_name=None, dir_name=None):
        """ takes data from json files in dir ../data"""
        if dir_name is not None:
            self.dir_name = dir_name
        if file_name:
            file_name_type = file_name.split(".")[-1]
            if file_name_type != "json":
                file_name += ".json"
        try:
            up_up_dir = os.path.dirname(os.path.dirname(__file__))
            json_file = os.path.join(up_up_dir, self.dir_name, file_name)
            with open(json_file, 'r') as jf:
                data = json.load(jf)
            return dict(data)
        except FileNotFoundError as e:
            self.logger.debug(f"File not found error json file: {e}")
            return None


if __name__ == '__main__':
    connector = ConnPgsqlJson()
    # ans = connector.get_fields_from_json("product_fields.json")
    # ans = connector.send_set_request("CREATE TABLE testtable (i integer);")
    # print(ans)
    ans = connector.get_json_files_list()
    print(ans)
    ans = connector.get_all_dicts_in_dir()
    print(ans)
