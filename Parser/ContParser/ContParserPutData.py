from Parser.ContParser.ContParserMainClass import ContParserMainClass
import pandas as pd
from datetime import datetime


class ContParserPutData(ContParserMainClass):
    columns_dict = ["on_date", "usd_840", "eur_978", "cny_156", "kzt_398", "jpy_392", "try_949", "qar_634", "aed_784", "byn_933"]
    def __init__(self):
        super().__init__()

    def get_parsed_data_on_date(self, on_date: datetime = None):
        from Parser.ConnParser.ConnParserExchange import ConnParserExchange
        parsed_df = ConnParserExchange().exchange_course_on_date(on_date)


if __name__ == '__main__':
    connector = ContParserPutData()
