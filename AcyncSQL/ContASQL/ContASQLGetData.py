from AcyncSQL.ContASQL.ContASQLMainClass import ContASQLMainClass
from AcyncSQL.ConnASQL.ConnASQLDataGet import ConnASQLDataGet
import asyncio

class ContASQLGetData(ContASQLMainClass, ConnASQLDataGet):
    def __init__(self):
        super().__init__()

    async def async_get_table_data(self, table_name: str):
        result = await asyncio.create_task(self.get_all_data_from_table_with_path(table_name))
        return result

async def main():
    req_dict = {
        'table_name': 'payments_in_table',
        'col_list': ['agent', 'sum', 'created'],
        'date_col': 'created',
        'from_date': '2023-06-01 00:00:00',
        'to_date': '2023-07-01 23:59:59',
        'to_file': True,
    }
    tasks_list = list()
    tasks_list.append(controller.get_col_data_from_table_date_filtered(**req_dict))
    req_dict['table_name'] = 'payments_out_table'
    tasks_list.append(controller.get_col_data_from_table_date_filtered(**req_dict))
    req_dict['table_name'] = 'packlists_in_table'
    tasks_list.append(controller.get_col_data_from_table_date_filtered(**req_dict))
    req_dict['table_name'] = 'packlists_out_table'
    tasks_list.append(controller.get_col_data_from_table_date_filtered(**req_dict))
    result = await asyncio.gather(*tasks_list)
    return result

if __name__ == '__main__':
    controller = ContASQLGetData()

    loop = asyncio.new_event_loop()
    data = loop.run_until_complete(main())
    print(data)

    # # loop.run_until_complete(connector.create_connection())
    # # loop.run_until_complete(connector.close_connection())
    # loop.run_until_complete(controller.get_table_data('pgsql_service_fields'))

