from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass

import datetime
import os
import importlib

class ModALGenBaseYear(ModALGenMainClass):
    """ create new base model for current year"""
    def __init__(self):
        super().__init__()

    def create_new_model_file(self, table_year: datetime = None, table_name: str = None):
        models_dir = "ModAL"
        models_module = "PgsqlAlchemy.ModAL"
        if not table_year:
            table_year = datetime.datetime.now().year
        if not table_name:
            table_name = "daily_profit"
        col_names_list = self.make_list_of_days(table_year=table_year)
        model_name = f"ModALDailyProfitY{table_year}"
        # model_dict = self.prepare_model_in_json(file_name=file_name)
        header = f"# !!!used SQLAlchemy 2.0.18\n" \
                 f"from sqlalchemy import create_engine, inspect\n" \
                 f"from sqlalchemy import Column, Integer, Double, DateTime\n" \
                 f"from sqlalchemy.orm import DeclarativeBase\n\n" \
                 f"from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass\n" \
                 f"__url = ConnALMainClass().get_url()\n" \
                 f"engine = create_engine(__url)\n\n" \
                 f"class Base(DeclarativeBase):\n\tpass\n\n" \
                 f"class {model_name}(Base):\n" \
                 f"\t__tablename__ = '{table_name}_{table_year}'\n" \

        body = f"\tposition_id = Column(Integer, primary_key=True, autoincrement=True, " \
               f"unique=True, nullable=False, comment='Обязательное поле для всех таблиц, автоповышение')\n" \

        for col_name in col_names_list:
            body += f"\t{col_name} = Column(Double, nullable=False, default=0)\n"


        footer = f"\ndef create_new_table():\n" \
                 f"\tBase.metadata.create_all(engine)\n\n" \
                 f"def delete_table():\n" \
                 f"\tBase.metadata.drop_all(engine)\n\n" \
                 f"if __name__ == '__main__':\n" \
                 f"\tcreate_new_table()\n" \
                 f"\t# delete_table()\n"

        # save to python file
        up_up_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(up_up_dir, models_dir, f"{model_name}.py")
        with open(file_path, "w") as file1:
            # Writing data to a file
            file1.write(header + body + footer)

        # run creation
        module_str = f"{models_module}.{model_name}"
        module = importlib.import_module(module_str)
        model_create = getattr(module, "create_new_table")
        model_create()

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
    generator = ModALGenBaseYear()
    print(generator.make_list_of_days(table_year=datetime.datetime.now().year))
    print(generator.create_new_model_file(table_year=datetime.datetime.now().year))


