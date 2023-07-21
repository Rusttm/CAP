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

    def update_daily_profit(self, **kwargs):
        model_class_table = kwargs.get("model_class_table", None)
        from_date = self.request_last_update_date_from_event_table(table_name=model_class_table)
        yesterday_end = self.request_yesterday_end()
        # this module update only full dates, not end day
        to_date = kwargs.get("to_date", yesterday_end)
        ans = self.put_data_to_profit_table(from_date=from_date, to_date=to_date)
        event_dict = {
            "table_name": model_class_table,
            "description": f"inserted or updated {len(ans)}rows in profit tables",
            "event_from": f"updater {__class__.__name__}",
            "from_date": from_date,
            "to_date": to_date
        }
        self.write_event_to_service_table(**event_dict)
        return ans

    def write_event_to_service_table(self, **kwargs):
        table_name = kwargs.get("table_name", None)
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        eventer = ConnALEvent()
        ans = eventer.put_event_2service_table_updates(**kwargs)
        if table_name:
            eventer.clear_old_records_from_event_table(older_than_days=7, table_name=table_name)
        return ans


    def request_yesterday_end(self) -> datetime:
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        yesterday_year = yesterday.year
        yesterday_month = yesterday.month
        yesterday_day = yesterday.day
        yesterday_end = datetime.datetime(yesterday_year, yesterday_month, yesterday_day, 23, 59, 0)
        return yesterday_end

    def request_last_update_date_from_event_table(self, table_name) -> datetime:
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        service_event = ConnALEvent()
        try:
            # request last date of updated data
            from_date = service_event.get_last_update_date_from_service(event_table=table_name)
        except Exception as e:
            self.logger.error(f"{__class__.__name__} cant get last data update, error: {e}")
            from_date = datetime.datetime(2022, 12, 31, 0, 0, 0) #.strftime("%Y-%m-%d %H:%M:%S")
        return from_date

    def put_data_to_profit_table(self, table_year: datetime = None,
                            from_date: datetime = None,
                            to_date: datetime = None) -> list:
        # tables_list = self.get_all_tables_list()
        results_list = []
        from PgsqlAlchemy.ConnMS.ConnMSFilter import ConnMSFilter
        filtered_ms = ConnMSFilter()
        from PgsqlAlchemy.ConnAL.ConnALGenTable import ConnALGenTable
        table_filler = ConnALGenTable()
        if not from_date:
            # start_date = datetime.datetime(2020, 3, 17, 0, 0, 1)
            start_date = datetime.datetime(2022, 1, 1, 0, 0, 1)
        else:
            start_date = from_date

        if not to_date:
            # end_date = datetime.datetime(2023, 7, 7, 23, 59, 0)
            end_date = datetime.datetime(2022, 12, 31, 23, 59, 0)
        else:
            end_date = to_date
        work_year = start_date.year
        work_date = start_date
        model_class = self.get_model_class_and_create_if_not_exist(year=work_year)

        while work_date < end_date:
            next_date = work_date + datetime.timedelta(days=1)
            if work_date.year != work_year:
                work_year = work_date.year
                model_class = self.get_model_class_and_create_if_not_exist(year=work_year)

            req_dict = {"from_date": work_date,
                        "to_date": next_date,
                        "filter_field_name": self.filter_filed,
                        "url_table_name": self.config_req_url}
            data_list = filtered_ms.get_ms_request_with_date_filter(**req_dict)
            table_name = f"{self.table_base_name}_{work_year}"
            req_dict2 = {"table_name": table_name,
                         "col_name": f"day_{work_date.strftime('%Y_%m_%d')}",
                         "data_list": data_list,
                         "model_class": model_class}
            if data_list:
                ans = table_filler.put_data_in_daily_table(**req_dict2)
                date_str = work_date.strftime('%Y_%m_%d')
                print(f"column {date_str} updated: {ans}")
                results_list.append(dict({date_str: ans}))
            else:
                print(f"column {work_date.strftime('%Y_%m_%d')} has no data")
            time.sleep(1)
            work_date += datetime.timedelta(days=1)
        return results_list
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
    # print(generator.update_daily_profit(table_year=datetime.datetime.now().year))
    generator.logger.debug("testing ModALGenPutDailyProfit")