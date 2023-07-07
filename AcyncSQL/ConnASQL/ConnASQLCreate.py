import pandas
import  time
from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
import asyncio
import asyncpg

class ConnASQLCreate(ConnASQLMainClass):
    _conn = None
    __config_dict = dict()

    def __init__(self):
        super().__init__()
        self.__config_dict = self.get_conn_dict()

    async def test_connection(self):
        try:
            self._conn = await asyncpg.connect(**self.__config_dict)
            print("connection established")
            await self._conn.close()
            return True
        except Exception as e:
            print(f"connection cannot be established, error {e}")
            self.logger.warning(f"{__class__.__name__} cant create new connection error: {e}")
            return False

    async def create_table(self, table_name: str = None):
        if table_name:
            req_line = f"CREATE TABLE IF NOT EXISTS {table_name} ();"
            _conn = await asyncpg.connect(**self.__config_dict)
            table_data = await _conn.fetch(req_line)
            await _conn.close()
            return True
        return False

    async def create_table_with_position_id(self, table_name: str = None):
        if table_name:
            req_line = f"CREATE TABLE IF NOT EXISTS {table_name} (position_id SERIAL PRIMARY KEY);"
            _conn = await asyncpg.connect(**self.__config_dict)
            table_data = await _conn.fetch(req_line)
            await _conn.close()
            return True
        return False

    async def create_col_in_table(self, **kwargs):
        table_name = kwargs.get('table_name', None)
        col_name = kwargs.get('col_name', None)
        col_type = kwargs.get('col_type', None)
        col_default = kwargs.get('col_default', None)
        if table_name and col_name and col_type:
            if col_default:
                req_line = f"ALTER TABLE IF EXISTS {table_name} ADD IF NOT EXISTS {col_name} {col_type} NOT null DEFAULT {col_default};"
            else:
                req_line = f"ALTER TABLE IF EXISTS {table_name} ADD IF NOT EXISTS {col_name} {col_type};"
            _conn = await asyncpg.connect(**self.__config_dict)
            table_data = await _conn.fetch(req_line)
            await _conn.close()
            return True
        return False

    async def create_col_in_table_with_default(self, **kwargs):
        table_name = kwargs.get('table_name', None)
        col_name = kwargs.get('col_name', None)
        col_type = kwargs.get('col_type', None)
        col_default = kwargs.get('col_default', None)
        if table_name and col_name and col_type:
            req_line = f"ALTER TABLE IF EXISTS {table_name} ADD IF NOT EXISTS {col_name} {col_type} NOT null DEFAULT {col_default};"
            _conn = await asyncpg.connect(**self.__config_dict)
            table_data = await _conn.fetch(req_line)
            await _conn.close()
            return True
        return False

    async def mark_unique_col_in_table(self, **kwargs):
        table_name = kwargs.get('table_name', None)
        col_name = kwargs.get('col_name', None)
        if table_name and col_name:
            req_line = f"ALTER TABLE IF EXISTS {table_name} ADD UNIQUE ({col_name});"
            _conn = await asyncpg.connect(**self.__config_dict)
            table_data = await _conn.fetch(req_line)
            await _conn.close()
            return True
        return False


if __name__ == '__main__':
    controller = ConnASQLCreate()
    loop = asyncio.new_event_loop()
    start_time = time.time()
    req_dict = {
        'table_name': 'customers_daily_bal_table',
    }

    data = loop.run_until_complete(controller.create_table_with_position_id(**req_dict))
    print(f"task finished with data: {data}")

    req_dict = {
        'table_name': 'customers_daily_bal_table',
        'col_name': 'test_col',
        'col_type': 'TEXT',
    }
    data = loop.run_until_complete(controller.create_col_in_table(**req_dict))
    print(f"task finished with data: {data}")

    req_dict = {
        'table_name': 'customers_daily_bal_table',
        'col_name': 'test_col_default',
        'col_type': 'BIGINT',
        'col_default': 0
    }
    data = loop.run_until_complete(controller.create_col_in_table_with_default(**req_dict))
    print(f"task finished with data: {data}")

    req_dict = {
        'table_name': 'customers_daily_bal_table',
        'col_name': 'test_col',
    }
    data = loop.run_until_complete(controller.mark_unique_col_in_table(**req_dict))
    print(f"task finished with data: {data}")

    loop.close()



    print(f"tasks finnished in {round(time.time() - start_time, 2)}sec")
