from PgsqlAlchemy.ModAL.ModALMainClass import ModALMainClass
from PgsqlAlchemy.ModAL.ModALGetModFromJson import ModALGetModFromJson


class ModALMakeModFile(ModALMainClass, ModALGetModFromJson):
    def __init__(self):
        super().__init__()

    def make_model_py_file_from_json(self, file_name: str = None):
        model_dict = self.prepare_model_in_json(file_name=file_name)
        fields_dict = model_dict.get("data", None)
        header = f"# !!!used SQLAlchemy 2.0.18\n" \
                 f"from sqlalchemy import create_engine, inspect\n" \
                 f"from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint\n" \
                 f"from sqlalchemy import Column, Integer, String, JSON, DateTime\n" \
                 f"from sqlalchemy import Double, BigInteger, Uuid, Boolean\n" \
                 f"from sqlalchemy.dialects.postgresql import JSONB, ARRAY, insert\n" \
                 f"from sqlalchemy.ext.mutable import MutableList\n" \
                 f"from sqlalchemy.orm import DeclarativeBase\n\n" \
                 f"from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass\n" \
                 f"__url = ConnALMainClass().get_url()\n" \
                 f"engine = create_engine(__url)\n\n" \
                 f"class Base(DeclarativeBase):\n\tpass\n\n" \
                 f"class ModALBase_{model_dict.get('table')}_(Base):\n" \
                 f"\t__tablename__ = '{model_dict.get('table')}'\n" \
                 f"\t__table_args__ = (UniqueConstraint('id', name='unique_key_id'),)\n"

        body = ""
        for col_name, col_dict in fields_dict.items():
            ext_dict = col_dict.get("ext_prop", None)
            ext_str = ""
            if ext_dict:
                ext_list = [f'{key}={val}' for key, val in ext_dict.items()]
                ext_str = ", "
                ext_str = ext_str + ", ".join(ext_list)

            temp_str = f"\t{col_name} = Column({col_dict.get('pg_type', None)}" \
                       f"{ext_str}" \
                       f", comment='{col_dict.get('descr', '')}')\n"
            body = body + temp_str

        footer = f"\ndef create_new_table():\n" \
                 f"\tBase.metadata.create_all(engine)\n\n" \
                 f"def delete_table():\n" \
                 f"\tBase.metadata.drop_all(engine)\n\n" \
                 f"if __name__ == '__main__':\n" \
                 f"\tcreate_new_table()\n" \
                 f"\t# delete_table()\n"

        with open(f"ModALBase_{model_dict.get('table', 'name')}.py", "w") as file1:
            # Writing data to a file
            file1.write(header + body + footer)
        return True


if __name__ == '__main__':
    connector = ModALMakeModFile()
    # res = connector.get_json_files_list(dir_name="config/models")
    # print(res)

    res = connector.make_model_py_file_from_json(file_name='pgsql_service_model')
    print(res)
