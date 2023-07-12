from PgsqlAlchemy.ModALUpdaters.ModALUpdaterMainClass import ModALUpdaterMainClass
from PgsqlAlchemy.ContMS.ContMSGetFilteredData import ContMSGetFilteredData
import datetime

class ModALGetTableData(ModALUpdaterMainClass, ContMSGetFilteredData):
    models_dir = "config/models"
    def __init__(self):
        super().__init__()


    def get_data_for_update_insertion(self, table_name: str = None) -> list:
        """ automatically gets date from event table and request update data with"""
        # get information for requester: url_table_name and date_field(filter_field_name)
        from PgsqlAlchemy.ConnAL.ConnALJson import ConnALJson
        json_reader = ConnALJson()
        json_dict = json_reader.get_data_from_json(file_name=table_name, dir_name=self.models_dir)
        url_table_name = json_dict.get("config_url", None)
        filter_field_name = json_dict.get("date_field", None)

        # make connector to service event table
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        service_event = ConnALEvent()
        # run function
        # gets functon name from config
        # from PgsqlAlchemy.ConnMS.ConnMSReadJson import ConnMSReadJson
        # self.model_config = ConnMSReadJson().get_config_json_data(file_name=self.table_name)
        # table_data_function = self.model_config.get("ms_func", None)
        # from PgsqlAlchemy.ContMS.ContMSMain import ContMSMain
        # ms_controller = ContMSMain()
        # request_func = getattr(ms_controller, table_data_function)
        # req_data = request_func(from_date=from_date, to_date=to_date)
        try:
            # request last date of updated data
            from_date = service_event.get_last_update_date_from_service(event_table=table_name)
        except Exception as e:
            # self.logger.error(f"{__class__.__name__} cant get last data update, error: {e}")
            from_date = datetime.datetime(2018, 1, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
        to_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"requested customers balances: {from_date=} / {to_date=}")
        req_dict = {"from_date": from_date,
                    "to_date": to_date,
                    "filter_field_name": filter_field_name,
                    "url_table_name": url_table_name}
        from PgsqlAlchemy.ContMS.ContMSGetFilteredData import ContMSGetFilteredData
        req_data = ContMSGetFilteredData().get_ms_request_with_date_filter(**req_dict)
        return req_data

if __name__ == '__main__':
    connector = ModALGetTableData()
    print(connector.get_data_for_update_insertion(table_name="customers_bal_model"))