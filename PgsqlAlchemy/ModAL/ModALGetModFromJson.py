from PgsqlAlchemy.ConnAL.ConnALJson import ConnALJson
from PgsqlAlchemy.ModAL.ModALMainClass import ModALMainClass

class ModALGetModFromJson(ConnALJson):
    _mapper_file = "mapper.json"
    _dir_mapper_file = "config"
    def __init__(self):
        super().__init__()

    def get_all_models_dict_list(self) -> list:
        result_list = []
        dir_name = "config/models"
        ans = self.get_all_dicts_in_dir()
        for mod in ans:
            table = self.get_data_from_json(file_name=mod, dir_name=dir_name)
            result_list.append(table)
        return result_list

    def correct_model_in_json(self, file_name: str = None) -> dict:
        """ returns dict {field_name:{col_name:value,}} """
        # get mapper dict
        table = self.get_data_from_json(file_name=file_name)
        data_dict = table.get("data", None)
        for key, val_dict in data_dict.items():
            ms_type = val_dict.get("type", None)
            cur_pg_type = val_dict.get("pg_type", None)
            if not cur_pg_type:
                pg_type = self.map_pg_type(ms_type=ms_type)
                data_dict[key]["pg_type"] = pg_type
            else:
                pg_type = cur_pg_type

        self.save_model_dict_2json(file_name=file_name, data_dict=data_dict)

        return data_dict


    def map_pg_type(self, ms_type: str = None) -> str:
        map_dict = self.get_data_from_json(file_name=self._mapper_file, dir_name=self._dir_mapper_file)
        return map_dict.get(ms_type, None)





if __name__ == '__main__':
    connector = ModALGetModFromJson()
    # res = connector.correct_model_in_json(file_name='customers_bal_model')
    # print(res)
    # ans = connector.get_all_models_dict_list()
    # print(f"result operation : {ans}")

    ans = connector.correct_model_in_json(file_name='customers_bal_model')
    print(f"result operation : {ans}")
