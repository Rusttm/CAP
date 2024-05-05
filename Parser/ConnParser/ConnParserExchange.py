from Parser.ConnParser.ConnParserMainClass import ConnParserMainClass
import pandas as pd
from datetime import datetime
import requests
from lxml import html
import random
import os


class ConnParserExchange(ConnParserMainClass):
    tree = None
    url = "https://cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To="
    data_dir = "data"
    df = pd.DataFrame()
    work_date = datetime.now()
    columns_dict = None
    work_date_str = datetime.now().strftime("%d.%m.%Y")
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"]

    def __init__(self):
        super().__init__()

    def load_user_agents(self):
        user_agents = self.get_config().get("user_agents", None)
        if user_agents:
            self.user_agents = user_agents

    def load_url(self):
        url = self.get_config().get("cbr_url", None)
        if url:
            self.url = url

    def set_tree(self):
        self.load_user_agents()
        self.load_url()
        try:
            # Определение целевого URL
            url = self.url + self.work_date_str
            # Отправка HTTP GET запроса на целевой URL с пользовательским заголовком User-Agent
            response = requests.get(url, headers={'User-Agent': random.choice(self.user_agents)})
            if 200 <= response.status_code < 300:
                print("данные с сайта запрошены")
            # Парсинг HTML-содержимого ответа с помощью библиотеки lxml
            self.tree = html.fromstring(response.content)
        except Exception as e:
            print(f"cant parse site, error {e}")

    def exchange_parse(self):
        """parses to pandas table of exchange """
        self.set_tree()
        try:
            # Использование выражения XPath для выбора всех строк таблицы в пределах таблицы с классом 'records-table'
            table_rows = self.tree.xpath(".//table[@class='data']/tbody")
            table_columns = table_rows[0].xpath("./tr//th/text()")
            table_columns = self.get_config().get("df_columns")
            # Использование выражения XPath для выбора всего текстового содержимого элементов 'td' в первой строке таблицы
            rows = table_rows[0].xpath(".//tr[position() > 1]")
        except Exception as e:
            print(f"Cant parse tree for exchange course, error: {e}")
        else:
            # Запись даных в файл csv
            data_rows = [[str(s) for s in list(row.xpath(".//td/text()"))] for row in rows]
            self.df = pd.DataFrame(data_rows, columns=table_columns, index=None)

    def set_date(self, use_date: datetime = None):
        """ sets  self.work_date after input, or today date"""
        if use_date is None:
            date_req = input("Введите дату в формате 21.12.2022 (Ввод -пропустить): ")
        else:
            if use_date <= datetime.now():
                self.work_date = use_date
                self.work_date_str = use_date.strftime("%d.%m.%Y")
            return
        try:
            res_date = datetime.strptime(date_req, "%d.%m.%Y")
            if res_date.date() > datetime.now().date():
                raise ValueError(f"Можно посмотреть курс только до сегодняшнего дня: {res_date.date()}")
        except Exception as e:
            print(f"Ошибка ввода даты, error: {e}")
            print(f"Собираю курсы на сегодня: {self.work_date.date()}")
        else:
            self.work_date = res_date
            self.work_date_str = res_date.strftime("%d.%m.%Y")

    def exchange_course_on_date(self, on_date: datetime = None, to_file: bool = False) -> pd.DataFrame:
        """ saves table of courses on date in csv table """
        try:
            self.set_date(on_date)
            self.exchange_parse()
            self.logger.debug(f"{__class__.__name__} parsed site")
        except Exception as e:
            err_str = f"{__class__.__name__} Cannot parse, error, error: {e}"
            print(err_str)
            self.logger.error(err_str)
        else:
            if to_file:
                file_name = f"exchange_{self.work_date.strftime('%Y_%m_%d')}.csv"
                dir_file = os.path.dirname(os.path.dirname(__file__))
                file_path = os.path.join(dir_file, self.data_dir, file_name)
                self.df.to_csv(file_path, index=False)
                print(f"Данные успешно записаны в файл '{file_name}'")
        return self.df


if __name__ == '__main__':
    connector = ConnParserExchange()
    my_date = datetime(year=2020, month=11, day=15)
    print(connector.exchange_course_on_date(on_date=my_date, to_file=True))
