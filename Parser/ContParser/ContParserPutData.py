from Parser.ContParser.ContParserMainClass import ContParserMainClass
import pandas as pd
from datetime import datetime


class ContParserPutData(ContParserMainClass):
    columns_dict = None
    table_name = "exchange_courses_model"
    def __init__(self):
        super().__init__()

    def load_columns(self):
        self.columns_dict = self.get_config().get("table_columns")

    def get_parsed_data_on_date(self, on_date: datetime = None) -> tuple:
        self.load_columns()
        from Parser.ConnParser.ConnParserExchange import ConnParserExchange
        parsed_df = ConnParserExchange().exchange_course_on_date(on_date)
        columns_list = []
        values_list = []
        for df_col_name, table_col_name in self.columns_dict.items():
            columns_list.append(table_col_name)
            if df_col_name == "date":
                values_list.append(on_date)
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
            values_list.append(value/multiplication)
        return columns_list, values_list

    def put_exchange_data_2table(self, on_date: datetime = None):
        col_list, values_list = self.get_parsed_data_on_date(on_date)
        from Pgsql.ConnPgsql.ConnPgsqlDataPut import ConnPgsqlDataPut
        pgsql_connector = ConnPgsqlDataPut()
        pgsql_connector.put_data_2table(table_name=self.table_name, col_names_list=col_list, col_values_list=values_list)




if __name__ == '__main__':
    connector = ContParserPutData()
    my_date = datetime(year=2018, month=11, day=7)
    print(connector.put_exchange_data_2table(on_date=my_date))