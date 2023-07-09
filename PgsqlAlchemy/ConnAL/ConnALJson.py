from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass
import json
import os


class ConnALJson(ConnPgsqlMainClass):
    """ convert models from json file to models directory"""
    dir_name = "config"

    def __init__(self):
        super().__init__()
        self.dir_name = "config"

    def get_json_files_list(self, dir_name: str = None):
        """ gets files .json in ../data"""
        if dir_name is not None:
            self.dir_name = dir_name
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        files_list = os.listdir(os.path.join(up_up_dir, self.dir_name))
        json_files_list = [file for file in files_list if file.endswith(".json")]
        return json_files_list

    def get_all_dicts_in_dir(self, dir_name: str = None) -> list:
        """ """
        if dir_name is not None:
            self.dir_name = dir_name
        json_files_list = self.get_json_files_list(dir_name=self.dir_name)
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

    def save_model_dict_2json(self,
                              file_name: str = None,
                              data_dict: dict = None,
                              dir_name: str = None,):
        if file_name:
            try:
                if dir_name is not None:
                    self.dir_name = dir_name
                file_name_type = file_name.split(".")[-1]
                if file_name_type != "json":
                    file_name += ".json"
                up_up_dir = os.path.dirname(os.path.dirname(__file__))
                json_file = os.path.join(up_up_dir, self.dir_name, file_name)
                import json
                with open(json_file, 'w') as fp:
                    json.dump(data_dict, fp, ensure_ascii=False)
                return True
            except Exception as e:
                error_str = f"cant write file to {file_name}, error {e}"
                print(error_str)
                self.logger.error(error_str)
                return False
        else:
            error_str = f"{__class__.__name__} please, set file name"
            self.logger.error(error_str)
            return False

if __name__ == '__main__':
    connector = ConnALJson()
    ans = connector.get_data_from_json("product_fields.json")

    # ans = connector.send_set_request("CREATE TABLE testtable (i integer);")
    # print(ans)
    # ans = connector.get_json_files_list()
    # print(ans)
    ans = connector.get_all_dicts_in_dir()
    # for mod in ans:
    #     table = connector.get_data_from_json(file_name=mod, dir_name="config/models")
    #     print(table.get("data", None))
    print(ans)