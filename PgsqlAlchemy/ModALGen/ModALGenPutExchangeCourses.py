from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass
from PgsqlAlchemy.ConnAL.ConnALTable import ConnALTable
import datetime
import importlib
import time


class ModALGenPutExchangeCourses(ModALGenMainClass, ConnALTable):
    """ fill today report table daily_bal"""
    table_base_name = "exchange_courses_model"
    model_base_class_name = "ModALBaseExchangeCourse"
    models_module = "PgsqlAlchemy.ModAL"

    def __init__(self):
        super().__init__()

    def update_exchange_course(self, **kwargs):
        model_class_table = kwargs.get("model_class_table", None)
        ans = self.put_data_to_exchange_course_table()
        event_dict = {
            "table_name": model_class_table,
            "description": f"inserted or updated {len(ans)}rows in {model_class_table} table",
            "event_from": f"updater {__class__.__name__}",
            "from_date": datetime.datetime.now(),
            "to_date": datetime.datetime.now()
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

    def request_last_update_date_from_event_table(self, table_name) -> datetime:
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        service_event = ConnALEvent()
        try:
            # request last date of updated data
            from_date = service_event.get_last_update_date_from_service(event_table=table_name)
        except Exception as e:
            self.logger.error(f"{__class__.__name__} cant get last data update, error: {e}")
            from_date = datetime.datetime(2023, 12, 31, 0, 0, 0)  #.strftime("%Y-%m-%d %H:%M:%S")
        return from_date

    def put_data_to_exchange_course_table(self, **kwargs) -> list:
        # tables_list = self.get_all_tables_list()
        results_list = []
        from PgsqlAlchemy.ModALUpdaters.ModALUpdTable import ModALUpdTable
        pgsql_alchemy_connector = ModALUpdTable()
        model_class = self.get_model_class()
        from Parser.ContParser.ContParserPutData import ContParserPutData
        parser_cont = ContParserPutData()
        work_date_timestamp = self.request_last_update_date_from_event_table(self.table_base_name)
        work_date = datetime.datetime.strptime(str(work_date_timestamp), "%Y-%m-%d %H:%M:%S")
        # work_date = datetime.datetime.fromtimestamp(work_date_timestamp)
        now_date = datetime.datetime.now()
        data_list = []
        while work_date < now_date:
            work_date += datetime.timedelta(days=1)
            req_dict = parser_cont.get_parsed_data_on_date(on_date=work_date)
            data_list.append(req_dict)
        ans = pgsql_alchemy_connector.put_data_2table(list_of_dicts=data_list,
                                                      model_class=model_class,
                                                      model_class_table=self.table_base_name,
                                                      model_unique_col="on_date")
        results_list.append(ans)
        return results_list

    def get_model_class(self) -> object:
        model_class_name = f"{self.model_base_class_name}"
        module_str = f"{self.models_module}.{model_class_name}"
        module = importlib.import_module(module_str)
        model_class = getattr(module, model_class_name)
        return model_class


if __name__ == '__main__':
    generator = ModALGenPutExchangeCourses()
    print(generator.get_model_class())
    print(generator.update_exchange_course(model_class_table="exchange_courses_model"))
    generator.logger.debug("testing ModALGenPutExchangeCourses")
