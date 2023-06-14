import time

from AcyncSQL.ContASQL.ContASQLMainClass import ContASQLMainClass
import asyncio
class AsyncSQLMain(ContASQLMainClass):

    def __init__(self):
        super().__init__()

    def get_pd_data_from_table(self, table_name: str=None):
        from AcyncSQL.ContASQL.ContASQLGetData import ContASQLGetData
        new_loop = asyncio.new_event_loop()
        task = ContASQLGetData().async_get_table_data(table_name)
        pd_data = new_loop.run_until_complete(task)
        return pd_data

    async def async_get_pd_data_from_table_with_path(self, table_name: str=None):
        from AcyncSQL.ContASQL.ContASQLGetData import ContASQLGetData
        pd_data = await ContASQLGetData().async_get_table_data(table_name)
        return pd_data
def main():
    controller = AsyncSQLMain()
    start = time.time()
    data = controller.get_pd_data_from_table('payments_in_table')
    time1 = time.time()
    print(f"first request {time1-start}")
    data = asyncio.run(controller.async_get_pd_data_from_table_with_path('payments_in_table'))
    time2 = time.time()
    print(f"second request {time2-time1}")

if __name__ == '__main__':
    main()
