from PgsqlAlchemy.ModAL.ModALMainClass import ModALMainClass
from PgsqlAlchemy.ModAL.ModALGetModFromJson import ModALGetModFromJson


class ModALMakeModFile(ModALMainClass, ModALGetModFromJson):
    def __init__(self):
        super().__init__()

    def make_model_py_file(self, model_dict: dict = None):
        str_list = []
        model_dict = self.prepare_model_in_json(file_name='customers_bal_model')
        fields_dict = model_dict.get("data", None)
        header = f"# !!!used SQLAlchemy 2.0.18\n" \
                 f"from sqlalchemy import create_engine\n" \
                 f"from sqlalchemy import Column, Integer, String, JSON, DateTime, Double, BigInteger\n" \
                 f"from sqlalchemy.orm import DeclarativeBase\n\n" \
                 f"from sqlalchemy.orm import sessionmaker\n" \
                 f"from sqlalchemy.orm import mapped_column\n\n" \
                 f"from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass\n" \
                 f"__url = ConnALMainClass().get_url()\n" \
                 f"engine = create_engine(__url)\n" \
                 f"class Base(DeclarativeBase):\n\tpass\n\n" \
                 f"class {model_dict.get('table')}(Base):\n" \
                 f"\t__tablename__ = '{model_dict.get('table')}'\n"

        body = ""
        for col_name, col_dict in fields_dict.items():
            ext_dict = col_dict.get("ext_prop", None)
            ext_str = ""
            if ext_dict:
                ext_list = [f'{key}={val}' for key, val in ext_dict.items()]
                ext_str = ", "
                ext_str = ext_str + ", ".join(ext_list)

            temp_str = f"\t{col_name} = Column({col_dict.get('pg_type', None)}" \
                       f"{ext_str})\n"
            body = body + temp_str

        footer = f"\nBase.metadata.create_all(engine)\n"
        with open(f"customers_bal_model.py", "w") as file1:
            # Writing data to a file
            file1.write(header + body + footer)
        return True


if __name__ == '__main__':
    connector = ModALMakeModFile()
    res = connector.get_json_files_list(dir_name="config/models")
    print(res)

    res = connector.make_model_py_file()
    print(res)
