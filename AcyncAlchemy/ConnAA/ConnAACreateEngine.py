""" this module doesnt works"""


from AcyncAlchemy.ConnAA.ConnAAMainClass import ConnAAMainClass
import asyncio
import asyncpg
import pandas as pd
from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

class ConnAACreateEngine(ConnAAMainClass):
    _engine = None
    __url = None

    def __init__(self):
        super().__init__()
        self.__url = self.get_url()

    async def async_main(self) -> bool:
        table_name = 'payments_out_table'
        self._engine = create_async_engine( self.__url, echo=True)
        Base = declarative_base()
        async_session = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)
        conn = self._engine.begin()
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        # table1 = Table("test_table", meta, Column("name", String(50), primary_key=True))
        #
        # await conn_dsdb.start(meta.create_all)


    # async def create_test_table(self):
    #
    #
    #
    #         # await conn.execute(t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}])
        return True

def main():
    connector = ConnAACreateEngine()
    loop = asyncio.new_event_loop()
    task1 = connector.async_main()
    # task2 = connector.create_test_table()
    result = loop.run_until_complete(task1)
    loop.close()
    print(result)


if __name__ == '__main__':
    main()
    import sqlalchemy
    print(sqlalchemy.__version__)

