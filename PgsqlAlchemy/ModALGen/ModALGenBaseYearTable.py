from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass

import datetime
import os
import importlib
import json


class ModALGenBaseYearTable(ModALGenMainClass):
    """ create new base model for current year"""
    models_dir = "ModAL"
    json_models_dir = "config/models"
    models_module = "PgsqlAlchemy.ModAL"

    def __init__(self):
        super().__init__()

    def create_new_profit_year(self, table_year: datetime = None) -> bool:
        if not table_year:
            table_year = datetime.datetime.now().year
        table_name = "daily_profit_model"
        model_name = f"ModALBaseDailyProfitY{table_year}"
        result = self.create_new_yearly_model_py_file(table_year, table_name, model_name)
        return result

    def create_new_bal_year(self, table_year: datetime = None) -> bool:
        if not table_year:
            table_year = datetime.datetime.now().year
        table_name = "daily_bal_model"
        model_name = f"ModALBaseDailyBalY{table_year}"
        result = self.create_new_yearly_model_py_file(table_year, table_name, model_name)
        return result

    def create_new_yearly_model_py_file(self, table_year: datetime = None,
                                        table_name: str = None,
                                        model_name: str = None) -> bool:
        col_names_list = self.make_list_of_days(table_year=table_year)
        req_dict = {'table_name': table_name,
                    'table_year': table_year,
                    'model_name': model_name,
                    'col_names_list': col_names_list}
        self.create_new_yearly_model_json_file(**req_dict)
        header = f"# !!!used SQLAlchemy 2.0.18\n" \
                 f"from sqlalchemy import create_engine, inspect\n" \
                 f"from sqlalchemy import Column, Integer, Double, DateTime, String\n" \
                 f"from sqlalchemy.dialects.postgresql import JSONB\n" \
                 f"from sqlalchemy.orm import DeclarativeBase\n\n" \
                 f"from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass\n" \
                 f"__url = ConnALMainClass().get_url()\n" \
                 f"engine = create_engine(__url)\n\n" \
                 f"class Base(DeclarativeBase):\n\tpass\n\n" \
                 f"class {model_name}(Base):\n" \
                 f"\t__tablename__ = '{table_name}_{table_year}'\n" \

        body = f"\tposition_id = Column(Integer, primary_key=True, autoincrement=True, " \
               f"unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')\n" \
               f"\tcounterparty = Column(JSONB, unique=True, " \
               f"nullable=False, comment='Контрагент. Подробнее тут Обязательное при ответе')\n" \
               f"\tname = Column(String)\n" \
               f"\tupdate = Column(DateTime, nullable=False, comment='Дата расчета (конец дня)')\n"
        for col_name in col_names_list:
            body += f"\t{col_name} = Column(Double, nullable=False, default=0, comment='прибыль на дату')\n"

        footer = f"\ndef create_new_table():\n" \
                 f"\tBase.metadata.create_all(engine)\n\n" \
                 f"def delete_table():\n" \
                 f"\tBase.metadata.drop_all(engine)\n\n" \
                 f"if __name__ == '__main__':\n" \
                 f"\tcreate_new_table()\n" \
                 f"\t# delete_table()\n"

        # save to python file
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(up_up_dir, self.models_dir, f"{model_name}.py")
        with open(file_path, "w") as file1:
            # Writing data to a file
            file1.write(header + body + footer)

        # run creation
        module_str = f"{self.models_module}.{model_name}"
        module = importlib.import_module(module_str)
        model_create = getattr(module, "create_new_table")
        model_create()

        return True

    def create_new_yearly_model_json_file(self, **kwargs)-> bool:

        table_year = kwargs.get("table_year")
        table_name = kwargs.get("table_name")
        model_name = kwargs.get("model_name")
        col_names_list = kwargs.get("col_names_list")
        json_class_dict = dict()
        json_class_dict["table"] = f'{table_name}_{table_year}'
        json_class_dict["model_class"] = model_name
        json_class_dict.update(dict({"req_func": "get_profit_by_cust_list",
                                     "date_field": "momentFrom_momentTo",
                                     "config_url": "url_profit_by_cust_list",
                                     "unique_col": "counterparty",
                                     "updated": ""}))

        data_dict = dict()
        data_dict.update(dict({
            "position_id": {"type": "Int",
                            "pg_type": "Integer",
                            "is_id": "True",
                            "filter": "= != < > <= >=",
                            "descr": "Обязательное поле для всех таблиц, автоповышение",
                            "ext_prop": {
                                "primary_key": "True",
                                "autoincrement": "True",
                                "unique": "True",
                                "nullable": "False"}}}))

        data_dict.update(dict({
            "counterparty": {"type": "Object",
                            "pg_type": "JSONB",
                            "is_id": "True",
                            "filter": "= != < > <= >=",
                            "descr": "meta клиента",
                            "ext_prop": {
                                "unique": "True",
                                "nullable": "False"}}}))

        data_dict.update(dict({
            "name": {"type": "String",
                             "pg_type": "String",
                             "filter": "= != < > <= >=",
                             "descr": "название клиента"}}))

        data_dict.update(dict({
            "update": {"type": "DateTime",
                            "pg_type": "DateTime",
                            "filter": "= != < > <= >=",
                            "descr": "дата расчета приыли"}}))

        for col_name in col_names_list:
            data_dict.update((dict({col_name: {"type": "Float",
                                                     "pg_type": "Double",
                                                     "descr": f"прибыль за {col_name.split('_')[1:]}",}})))
        json_class_dict["data"] = data_dict
        # save to python file
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        json_file_path = os.path.join(up_up_dir, self.json_models_dir, f"{table_name}_{table_year}.json")
        with open(json_file_path, "w") as jf:
            # Writing data to a file
            json.dump(json_class_dict, jf, ensure_ascii=False)

        return True

    def make_list_of_days(self, table_year: datetime = None):
        result_list = list()
        start_year_date = datetime.datetime(table_year, 1, 1, 0, 0, 1)
        end_year = datetime.datetime(table_year, 12, 31, 11, 59, 59)

        col_date = start_year_date
        while col_date < end_year:
            col_name = col_date.strftime("day_%Y_%m_%d")
            col_date += datetime.timedelta(days=1)
            result_list.append(col_name)
        return result_list


if __name__ == '__main__':
    generator = ModALGenBaseYearTable()
    print(generator.make_list_of_days(table_year=datetime.datetime.now().year))
    print(generator.create_new_bal_year(table_year=datetime.datetime(2013, 1, 1).year))
    # print(generator.create_new_yearly_model_json_file(table_year=datetime.datetime(2013, 1, 1).year))
