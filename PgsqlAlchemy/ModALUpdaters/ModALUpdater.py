#!python
import sys
import os

cap_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

sys.path.append(cap_dir_path)

from PgsqlAlchemy.ModALUpdaters.ModALUpdaterMainClass import ModALUpdaterMainClass
import time
import importlib

class ModALUpdater(ModALUpdaterMainClass):
    models_dir = os.path.join("config", "models")
    gen_module = "PgsqlAlchemy.ModALGen"
    allowed_arguments = ["daily", "hourly", "ondemand", "test"]
    model_dict = None   # dictionary from model json
    def __init__(self):
        super().__init__()

    def db_updater(self, period: str = None):
        """ full daily hourly and ondemand updater"""
        ans_list = list()
        # check period
        if period not in self.allowed_arguments:
            err_str = f"{__class__.__name__} not allowed argument {period} in updater, allowed only: {self.allowed_arguments}"
            self.logger.debug(err_str)
            return ans_list

        # load updater
        from PgsqlAlchemy.ModALUpdaters.ModALUpdTable import ModALUpdTable
        updater_module = ModALUpdTable()
        # get all models in directory
        from PgsqlAlchemy.ConnAL.ConnALJson import ConnALJson
        json_loader = ConnALJson()
        # load list of model names from directory
        all_models = json_loader.get_all_dicts_in_dir(dir_name=self.models_dir)
        # from every json config reads type of refreshing table
        for model in all_models:
            # get all data from file
            self.model_dict = json_loader.get_data_from_json(file_name=model, dir_name=self.models_dir)
            # get update property: daily, hourly, ondemand
            updated_key = self.model_dict.get("updated", None)
            # if it not equal requested - skips
            if updated_key != period:
                # skip table if period not equal table period
                continue
            # other points: "ondemand", "test" - generates tables, not MS API requested
            if updated_key in ["ondemand", "test"]:
                ans = self.generated_tables_updater()
                ans_list.append(dict({self.model_dict.get("table", None): ans}))

            # if daily key -> run updater
            elif updated_key in ["daily", "hourly"]:
                """ this part for hourly/daily requests in MS 
                you must set 'url' of MS_API in json """
                # load from json keys
                # it uses updaters by ModALUpdTable
                model_class_table = self.model_dict.get("table", "unknown_table")
                model_class_name = self.model_dict.get("model_class", None)
                model_unique_col = self.model_dict.get("unique_col", None)
                ans = updater_module.update_model_table(model_class_name=model_class_name,
                                                        model_unique_col=model_unique_col,
                                                        model_class_table=model_class_table)
                ans_list.append(dict({self.model_dict.get("table", "unknown_table"): ans}))

        return ans_list

    def generated_tables_updater(self) -> dict:
        """ this updater reads from json file:
        class ('updater_class') + method ('updater_func') and runs it """
        updater_class_name = self.model_dict.get("updater_class", None)
        updater_function_name = self.model_dict.get("updater_func", None)
        # makes and run updater function (updater_conn)
        # with class generator in self.gen_module = "PgsqlAlchemy.ModALGen"
        module_str = f"{self.gen_module}.{updater_class_name}"
        module = importlib.import_module(module_str)
        updater_class = getattr(module, updater_class_name)
        updater_class_obj = updater_class()
        updater_conn = getattr(updater_class_obj, updater_function_name)
        # create dict with parameters
        request_dict = {
            "model_class_table": self.model_dict.get("table", None),
            "updater_class_name": updater_class_name,
            "updater_function_name": updater_function_name,
            "unique_col": self.model_dict.get("unique_col", None),
            "date_field": self.model_dict.get("date_field", None),
            "config_url": self.model_dict.get("config_url", None),
            "model_tables": self.model_dict.get("model_tables", None),
            "service_url": self.model_dict.get("service_url", None),

        }
        ans = updater_conn(**request_dict)
        return ans

    def daily_updater(self):
        """ updates only MS API requests"""
        return self.db_updater(period="daily")

    def hourly_updater(self):
        """ updates only MS API requests"""
        return self.db_updater(period="hourly")

    def ondemand_updater(self):
        return self.db_updater(period="ondemand")

    def test_updater(self):
        return self.db_updater(period="test")


def main():
    allowed_arguments = ["daily", "hourly", "ondemand", "test"]
    results_list = []
    start = time.time()
    updater = ModALUpdater()
    # total arguments
    n = len(sys.argv)
    if n<=1:
        print(f"please send update period like {allowed_arguments}")
    else:
        for command_argument in sys.argv[1:]:
            if command_argument in allowed_arguments:
                res=updater.db_updater(period=command_argument)
                results_list.append(res)
            else:
                print(f"argument: {command_argument} is not update period")
    print(f"update time: {round(time.time() - start, 2)}sec\n")
    print(f"update result: {results_list}\n")
    return results_list




if __name__ == '__main__':
    # main()

    updater = ModALUpdater()
    # connector.logger.info("testing ModALFillCustBal")
    # print(f"logger file name: {connector.logger_name}")
    # print(connector.get_last_update_date_from_service("customers_bal_table"))
    # print(connector.get_data_for_insertion("customers_bal_model"))
    start = time.time()
    # res = updater.update_customers_balance()
    # print(f"function result: {res}")
    # res = updater.clear_old_events()
    # print(f"function result: {res}")
    time1 = time.time()
    # res = updater.db_updater(period="hourly")
    # print(f"hourly updates ({round(time.time() - start, 2)}sec) result: {res}")

    # res = updater.db_updater(period="daily")
    # print(f"daily updates ({round(time.time() - time1, 2)}sec) result: {res}")

    # res = updater.db_updater(period="test")
    res = updater.db_updater(period="ondemand")
    print(f"ondemand updates ({round(time.time() - time1, 2)}sec) result: {res}")

    print(f"function time = {round(time.time() - start, 2)}sec")

    print(updater.ondemand_updater())