from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass
from PgsqlAlchemy.ConnAL.ConnALTable import ConnALTable
import datetime
import importlib
import time

class ModALGenPutDailyProfit(ModALGenMainClass, ConnALTable):
    """ fulfill report table daily_profit"""
    table_base_name = "daily_profit_model"
    req_table = "profit_bycust_model"
    filter_filed = "momentFrom_momentTo"
    config_req_url = "url_profit_by_cust_list"
    model_base_class_name = "ModALBaseDailyProfitY"
    models_module = "PgsqlAlchemy.ModAL"

    def __init__(self):
        super().__init__()

    def get_data_for_update_daily_profit(self, table_year: datetime = None):
        tables_list = self.get_all_tables_list()

        from PgsqlAlchemy.ConnMS.ConnMSFilter import ConnMSFilter
        filterred_ms = ConnMSFilter()
        from PgsqlAlchemy.ConnAL.ConnALGenTable import ConnALGenTable
        table_filler = ConnALGenTable()
        start_date = datetime.datetime(2020, 3, 17, 0, 0, 1)
        # end_date = datetime.datetime(2023, 7, 7, 23, 59, 0)
        end_date = datetime.datetime(2020, 12, 31, 23, 59, 0)
        work_year = start_date.year
        work_date = start_date
        model_class = self.get_model_class_and_create_if_not_exist(year=work_year)
        while work_date < end_date:
            next_date = work_date + datetime.timedelta(days=1)
            if work_date.year != work_year:
                model_class = self.get_model_class_and_create_if_not_exist(year=work_year)

            req_dict = {"from_date": work_date,
                        "to_date": next_date,
                        "filter_field_name": self.filter_filed,
                        "url_table_name": self.config_req_url}
            data_list = filterred_ms.get_ms_request_with_date_filter(**req_dict)

            req_dict2 = {"table_name": f"{self.table_base_name}_{work_year}",
                         "col_name": f"day_{work_date.strftime('%Y_%m_%d')}",
                         "data_list": data_list,
                         "model_class": model_class}
            if data_list:
                ans = table_filler.put_data_in_daily_table(**req_dict2)
                print(f"column {work_date.strftime('%Y_%m_%d')} updated: {ans}")
            else:
                print(f"column {work_date.strftime('%Y_%m_%d')} has no data")
            time.sleep(1)
            work_date += datetime.timedelta(days=1)

        return data_list
    def get_model_class_and_create_if_not_exist(self, year: datetime = None) -> object:
        from PgsqlAlchemy.ModALGen.ModALGenBaseYearTable import ModALGenBaseYearTable
        table_generator = ModALGenBaseYearTable()
        table_name = f"{self.table_base_name}_{year}"
        # create class if doesnt exist
        if not self.check_table_exist(table_name):
            print(f"{table_name} doesnt exist")
            table_generator.create_new_profit_year(table_year=year)
            print(f"{table_name} exist!")
        model_class_name = f"{self.model_base_class_name}{year}"
        module_str = f"{self.models_module}.{model_class_name}"
        module = importlib.import_module(module_str)
        model_class = getattr(module, model_class_name)
        return model_class




if __name__ == '__main__':
    generator = ModALGenPutDailyProfit()
    print(generator.get_data_for_update_daily_profit(table_year=datetime.datetime.now().year))
