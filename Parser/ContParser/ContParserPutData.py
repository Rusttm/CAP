from Parser.ContParser.ContParserMainClass import ContParserMainClass
import pandas as pd
from datetime import datetime, timedelta, date


class ContParserPutData(ContParserMainClass):
    columns_dict = None
    table_name = "exchange_courses_model"
    model_class = None

    def __init__(self):
        super().__init__()

    def load_columns(self):
        self.columns_dict = self.get_config().get("table_columns")

    def load_model_class_obj(self):
        from PgsqlAlchemy.ModAL.ModALBaseExchangeCourse import ModALBaseExchangeCourse
        model_obj = ModALBaseExchangeCourse
        self.model_class = model_obj

    def get_parsed_data_on_date(self, on_date: datetime = None) -> dict:
        self.load_columns()
        from Parser.ConnParser.ConnParserExchange import ConnParserExchange
        parsed_df = ConnParserExchange().exchange_course_on_date(on_date)
        data_dict = dict()
        for df_col_name, table_col_name in self.columns_dict.items():
            if df_col_name == "date":
                data_dict[table_col_name] = on_date.strftime("%Y.%m.%d")
                continue
            try:
                value_str = str(parsed_df["course"][parsed_df["tag"] == df_col_name].values[0])
                value = float(value_str.replace(",", "."))
                multiplication = int(parsed_df["mult"][parsed_df["tag"] == df_col_name].values[0])
            except IndexError:
                err_str = f"cant find {df_col_name}"
                self.logger.debug(err_str)
                print(err_str)
                value = 0
                multiplication = 1
            data_dict[table_col_name] = value / multiplication
        return data_dict

    def put_exchange_data_2table(self, on_date: datetime = None):
        data_dict = self.get_parsed_data_on_date(on_date)
        self.load_model_class_obj()
        from PgsqlAlchemy.ModALUpdaters.ModALUpdTable import ModALUpdTable
        pgsql_alchemy_connector = ModALUpdTable()
        pgsql_alchemy_connector.put_data_2table(list_of_dicts=[data_dict],
                                                model_class=self.model_class,
                                                model_class_table=self.table_name,
                                                model_unique_col="on_date")


if __name__ == '__main__':
    import time
    import random

    connector = ContParserPutData()
    start_date = datetime(year=2018, month=11, day=9)
    end_date = datetime(year=2018, month=12, day=31)
    while start_date < end_date:
        time.sleep(random.randint(0, 3))
        start_date += timedelta(days=1)
        print(connector.put_exchange_data_2table(on_date=start_date))
