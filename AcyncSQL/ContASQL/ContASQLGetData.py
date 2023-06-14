from AcyncSQL.ContASQL.ContASQLMainClass import ContASQLMainClass
from AcyncSQL.ConnASQL.ConnASQLDataGet import ConnASQLDataGet
import asyncio

class ContASQLGetData(ContASQLMainClass, ConnASQLDataGet):
    def __init__(self):
        super().__init__()

    async def async_get_table_data(self, table_name: str):
        result = await asyncio.create_task(self.get_all_data_from_table_with_path(table_name))
        return result


if __name__ == '__main__':
    controller = ContASQLGetData()
    # loop = asyncio.new_event_loop()
    # # loop.run_until_complete(connector.create_connection())
    # # loop.run_until_complete(connector.close_connection())
    # loop.run_until_complete(controller.get_table_data('pgsql_service_fields'))
    print(asyncio.run(controller.get_table_data('pgsql_service_fields')))