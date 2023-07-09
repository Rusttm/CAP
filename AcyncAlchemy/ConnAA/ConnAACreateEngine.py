from AcyncAlchemy.ConnAA.ConnAAMainClass import ConnAAMainClass
import asyncio

from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine


class ConnAACreateEngine(ConnAAMainClass):
    _engine = None
    __url = None

    def __init__(self):
        super().__init__()
        self.__url = self.get_url()

    async def async_main(self) -> bool:
        self._engine = create_async_engine(
            "postgresql+asyncpg://scott:tiger@localhost/test",
            echo=True,
        )
        return True

    async def create_test_table(self):
        meta = MetaData()
        table1 = Table("test_table", meta, Column("name", String(50), primary_key=True))
        async with self._engine.begin() as conn:
            await conn.run_sync(meta.create_all)
            # await conn.execute(t1.insert(), [{"name": "some name 1"}, {"name": "some name 2"}])


def main():
    connector = ConnAACreateEngine()
    loop = asyncio.new_event_loop()
    task1 = connector.async_main()
    task2 = connector.create_test_table()
    result = loop.run_until_complete(task2)
    loop.close()
    print(result)


if __name__ == '__main__':
    # main()
    import sqlalchemy
    print(sqlalchemy.__version__)

