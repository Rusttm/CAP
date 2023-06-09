from PgsqlAlchemy.ModALUpdaters.ModALUpdaterMainClass import ModALUpdaterMainClass
import time
import importlib

class ModALUpdater(ModALUpdaterMainClass):
    models_dir = "config/models"
    gen_module = "PgsqlAlchemy.ModALGen"
    def __init__(self):
        super().__init__()

    def db_updater(self, period: str = None):
        """ daily updater"""
        ans_list = list()
        # load updater
        from PgsqlAlchemy.ModALUpdaters.ModALUpdTable import ModALUpdTable
        updater_module = ModALUpdTable()
        # get all models in directory
        from PgsqlAlchemy.ConnAL.ConnALJson import ConnALJson
        json_loader = ConnALJson()
        # load list of model names from directory
        all_models = json_loader.get_all_dicts_in_dir(dir_name=self.models_dir)
        for model in all_models:
            model_dict = json_loader.get_data_from_json(file_name=model, dir_name=self.models_dir)
            updated_key = model_dict.get("updated", None)
            if updated_key in ["ondemand"]:
                updater_class_name = model_dict.get("updater_class", None)
                updater_function_name = model_dict.get("updater_func", None)
                # make and run updater function
                module_str = f"{self.gen_module}.{updater_class_name}"
                module = importlib.import_module(module_str)
                updater_class = getattr(module, updater_class_name)
                updater_class_obj = updater_class()
                updater_conn = getattr(updater_class_obj, updater_function_name)
                request_dict = {
                    "model_class_table": model_dict.get("table", None),
                    "updater_class_name": updater_class_name,
                    "updater_function_name": updater_function_name,
                    "unique_col": model_dict.get("unique_col", None)
                }
                ans = updater_conn(**request_dict)
                ans_list.append(ans)

            # if daily key -> run updater
            elif updated_key in ["daily", "hourly"]:
                # load from json keys
                model_class_table = model_dict.get("table", None)
                model_class_name = model_dict.get("model_class", None)
                model_unique_col = model_dict.get("unique_col", None)
                ans = updater_module.update_model_table(model_class_name=model_class_name,
                                                        model_unique_col=model_unique_col,
                                                        model_class_table=model_class_table)
                ans_list.append(ans)
        return ans_list

    def daily_updater(self):
        return self.db_updater(period="daily")

    def hourly_updater(self):
        return self.db_updater(period="hourly")

    def ondemand_updater(self):
        return self.db_updater(period="ondemand")



    # def update_customers_balance(self):
    #     table_name = "customers_bal_model"
    #     from PgsqlAlchemy.ModALUpdaters.ModALUpdCustBal import ModALUpdCustBal
    #     res = ModALUpdCustBal().update_cust_bal()
    #     from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
    #     ConnALEvent().clear_old_records_from_event_table(older_than_days=7, table_name=table_name)
    #     return res
    #
    # def clear_old_events(self) -> str:
    #     from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
    #     ConnALEvent().clear_old_records_from_event_table(older_than_days=7, table_name="customers_bal_model")
    #     return f"service event table cleared"


if __name__ == '__main__':
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
    res = updater.db_updater(period="hourly")
    print(f"hourly updates ({round(time.time() - start, 2)}sec) result: {res}")

    res = updater.db_updater(period="daily")
    print(f"daily updates ({round(time.time() - time1, 2)}sec) result: {res}")

    print(f"function time = {round(time.time() - start, 2)}sec")