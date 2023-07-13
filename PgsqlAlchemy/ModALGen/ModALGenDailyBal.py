from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass
from PgsqlAlchemy.ModAL.ModALBaseDailyBal import ModALBaseDailyBal
from sqlalchemy import create_engine, MetaData, Table, Column, Double, Text
from sqlalchemy import select, text, column, Integer, schema, event, DDL, String
from sqlalchemy.dialects.postgresql import JSONB
from alembic import op
from sqlalchemy.orm import sessionmaker
from alembic.migration import MigrationContext
from alembic.operations import Operations

from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
__url = ConnALMainClass().get_url()
engine = create_engine(__url)


class ModALGenDailyBal(ModALGenMainClass, ModALBaseDailyBal):
    def __init__(self):
        super().__init__()

    def make_new_col_in_daily_bal(self, col_name: str = None):
        table_name = 'daily_bal_model'
        column_name = "inn_132102258526"
        column_descr = "ИП Денискина"
        # version1
        new_col = Column(column_name, Double, default=0, nullable=False, comment=column_descr, server_default=text(0))
        metadata_obj = MetaData()
        table_metadata = Table(table_name, metadata_obj, new_col)  # Table object
        metadata_obj.create_all(engine)
        print(table_metadata)

        # version 2 create only new table
        # metadata_obj = MetaData()
        # table_metadata = Table("test_table2", metadata_obj, Column("test_col", Integer),)  # Table object
        # metadata_obj.create_all(bind=engine)
        # print(table_metadata.columns)
        # print(table_metadata.metadata.create_all(bind=engine))

        # version 3
        # connection = engine.connect()
        # query = text(f"ALTER TABLE IF EXISTS test_table ADD IF NOT EXISTS test_col TEXT;")
        # # query = text(f'SELECT * FROM {table_name}')
        # ex_result = connection.execute(query)
        # connection.close()
        # print(f"result {ex_result.context}")

        # version 4
        # connection = engine.connect()
        # metadata_obj = MetaData()
        # table = Table(table_name, metadata_obj)
        # col_obj = Column("test_col", Integer)
        # table.append_column(col_obj)
        # query = table.update()
        # connection.execute(query)

        # version 5
        # connection = engine.connect()
        # metadata_obj = MetaData()
        # table_my = Table(table_name, metadata_obj)
        # new_col = Column("test_col", Integer)
        # table_my.append_column(new_col)
        # metadata_obj.create_all(engine)

        # version 6
        # connection = engine.connect()
        # metadata_obj = MetaData()
        # table_my = Table(table_name, metadata_obj)
        # sel_ddl = DDL(f"ALTER TABLE IF EXISTS {table_name} ADD IF NOT EXISTS test_col TEXT;")
        # event.listen(table_my, "after_create", sel_ddl.execute_if(dialect=engine.dialect))
        # connection.execute(sel_ddl)
        # connection.close()
        # alembic.Operations().add_column(table_name=table_name, column=Column("test_col", Integer))

        # version 7
        # from https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.add_column
        # Create migration context
        # connection = engine.connect()
        # mc = MigrationContext.configure(engine.connect())
        # # Creation operations object
        # ops = Operations(mc)
        # # ops.add_column("test_table", Column(name="name", type_=String()))
        # ops.add_column(table_name, Column(name="name", type_=String()))
        # connection.execute()
        # connection.close()
        return True


    def get_columns_list(self, table_name: str = None):

        # version 1 doesnt works with empty table
        # Session = sessionmaker(bind=engine)
        # session = Session()
        # qry_object = session.query(ModALBaseDailyBal)
        # session.commit()
        # print(qry_object)

        # version 2
        metadata = MetaData()  # extracting the metadata
        table_metadata = Table('daily_bal_model', metadata, autoload_with=engine)  # Table object
        # print(repr(metadata.tables['daily_bal_model']))
        return table_metadata.columns.keys()


if __name__ == '__main__':
    generator = ModALGenDailyBal()
    print(generator.get_columns_list('daily_bal_model'))
    # print(generator.make_new_col_in_daily_bal())
    print(generator.get_columns_list('daily_bal_model'))
