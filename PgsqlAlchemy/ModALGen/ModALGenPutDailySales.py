from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass
from PgsqlAlchemy.ConnAL.ConnALTable import ConnALTable
import datetime
import importlib
import time

class ModALGenPutDailySales(ModALGenMainClass, ConnALTable):
    """ fulfill report table daily_profit"""
    table_base_name = None  # = "daily_profit_model"
    # req_table = "profit_bycust_model"
    filter_filed = None  # "momentFrom_momentTo"
    config_req_url = None  # "url_profit_by_cust_list"
    service_url = None
    model_base_class_name = None  # "ModALBaseDailyStockStoreY"
    unique_col = None
    models_module = "PgsqlAlchemy.ModAL"

    def __init__(self):
        super().__init__()

    def update_daily_sales(self, **kwargs):
        # model_class_table = kwargs.get("model_class_table", None)
        self.filter_filed = kwargs.get("date_field", None)
        self.table_base_name = kwargs.get("model_class_table", None)
        self.config_req_url = kwargs.get("config_url", None)
        self.model_base_class_name = kwargs.get("model_tables", None)
        self.unique_col = kwargs.get("unique_col", None)
        self.service_url = kwargs.get("service_url", None)
        from_date = self.request_last_update_date_from_event_table(table_name=self.table_base_name)
        # from_date = datetime.datetime(2022, 1, 27)
        yesterday_end = self.request_yesterday_end()
        # this module update only full dates, not end day
        to_date = kwargs.get("to_date", yesterday_end)
        ans = self.put_data_to_daily_stock_store_table(from_date=from_date, to_date=to_date)
        event_dict = {
            "table_name": self.table_base_name,
            "description": f"inserted or updated {len(ans)}rows in {self.table_base_name} tables",
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

    def put_data_to_daily_stock_store_table(self, table_year: datetime = None,
                                            from_date: datetime = None,
                                            to_date: datetime = None) -> list:
        # tables_list = self.get_all_tables_list()
        results_list = []
        from PgsqlAlchemy.ConnMS.ConnMSFilter import ConnMSFilter
        filtered_ms = ConnMSFilter()
        from PgsqlAlchemy.ConnAL.ConnALGenDailySalesTable import ConnALGenDailySalesTable
        table_filler = ConnALGenDailySalesTable()
        if not from_date:
            # start_date = datetime.datetime(2020, 3, 17, 0, 0, 1)
            start_date = datetime.datetime(2021, 1, 1, 0, 0, 1)
        else:
            start_date = from_date

        if not to_date:
            # end_date = datetime.datetime(2023, 7, 7, 23, 59, 0)
            end_date = datetime.datetime(2021, 12, 31, 23, 59, 0)
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
            if not data_list:
                print(f"{self.config_req_url} has no data on {work_date.strftime('%Y_%m_%d')}date")
                time.sleep(1)
                work_date += datetime.timedelta(days=1)
                continue
            if self.service_url:
                req_dict["url_table_name"] = self.service_url
                req_dict["filter_field_name"] = None
                service_list = filtered_ms.get_ms_request_with_date_filter(**req_dict)
            else:
                service_list = None
            table_name = f"{self.table_base_name}_{work_year}"
            req_dict2 = {"table_name": table_name,
                         "col_name": f"day_{work_date.strftime('%Y_%m_%d')}",
                         "data_list": data_list,
                         "service_list": service_list,
                         "model_class": model_class,
                         "unique_col": self.unique_col
                         }
            ans = table_filler.put_data_in_daily_sales_table(**req_dict2)
            date_str = work_date.strftime('%Y_%m_%d')
            print(f"column {date_str} updated: {ans}")
            results_list.append(dict({date_str: ans}))
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
            table_generator.create_new_yearly_model_py_file(table_year=year,
                                                            table_name=self.table_base_name,
                                                            model_name=f"{self.model_base_class_name}{year}",
                                                            unique_col=self.unique_col)
            print(f"{table_name} created!")
        model_class_name = f"{self.model_base_class_name}{year}"
        module_str = f"{self.models_module}.{model_class_name}"
        module = importlib.import_module(module_str)
        model_class = getattr(module, model_class_name)
        return model_class




if __name__ == '__main__':
    generator = ModALGenPutDailySales()
    # print(generator.update_daily_stock_store(table_year=datetime.datetime.now().year))
    # generator.logger.debug("testing ModALGenPutDailyProfit")