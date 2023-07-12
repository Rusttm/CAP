from PgsqlAlchemy.ConnAL.ConnALJson import ConnALJson
from PgsqlAlchemy.ModAL.ModALMainClass import ModALMainClass
import os
class ModALGetModFromJson(ConnALJson):
    _mapper_file = "alchemy_mapper.json"
    _dir_mapper_file = "config"
    _models_dir = os.path.join("config", "models")
    def __init__(self):
        super().__init__()

    def get_all_models_dict_list(self) -> list:
        result_list = []
        ans = self.get_all_dicts_in_dir(dir_name=self._models_dir)
        for mod in ans:
            table = self.get_data_from_json(file_name=mod, dir_name=self._models_dir)
            result_list.append(table)
        return result_list

    def prepare_model_in_json(self, file_name: str = None) -> dict:
        """ prepare model json file for pgsql datatype:
        add pg_type
        add position_id column
        returns dict {field_name:{col_name:value,}} """
        # get mapper dict
        model_dict = self.get_data_from_json(file_name=file_name, dir_name=self._models_dir)
        data_dict = model_dict.get("data", None)

        if not data_dict.get("position_id", None):
            pos_id_dict = {"position_id": {"type": "Int",
                                           "pg_type": "Integer",
                                           "is_id": "True",
                                           "filter": "= != < > <= >=",
                                           "descr": "Обязательное поле для всех таблиц, автоповышение",
                                           "ext_prop": {"primary_key": "True",
                                                        "autoincrement": "True",
                                                        "unique": "True",
                                                        "nullable": "False"}
                                           }
                           }
            pos_id_dict.update(data_dict)
            data_dict = pos_id_dict

        for key, val_dict in data_dict.items():
            if key == "position_id":
                continue
            ms_type = val_dict.get("type", None)
            cur_pg_type = val_dict.get("pg_type", None)
            if not cur_pg_type:
                data_dict[key]["pg_type"] = self.map_pg_type(ms_type=ms_type)
            else:
                pg_type = cur_pg_type
                 # if you want to rewrite models pg_type
                # data_dict[key]["pg_type"] = self.map_pg_type(ms_type=ms_type)



        model_dict["data"] = data_dict
        self.save_model_dict_2json(file_name=file_name,
                                   data_dict=model_dict,
                                   dir_name=self._models_dir)

        return model_dict


    def map_pg_type(self, ms_type: str = None) -> str:
        map_dict = self.get_data_from_json(file_name=self._mapper_file, dir_name=self._dir_mapper_file)
        return map_dict.get(ms_type, None)





if __name__ == '__main__':
    connector = ModALGetModFromJson()
    res = connector.prepare_model_in_json(file_name='invout_model')
    print(res)
    # ans = connector.get_all_models_dict_list()
    # print(f'result operation : {ans}')

    # ans = connector.correct_model_in_json(file_name='customers_bal_model')
    # print(f"result operation : {ans}")
