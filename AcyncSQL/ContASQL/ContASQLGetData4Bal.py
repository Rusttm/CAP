from AcyncSQL.ContASQL.ContASQLMainClass import ContASQLMainClass
from AcyncSQL.ConnASQL.ConnASQLDataGet4Bal import ConnASQLDataGet4Bal
import asyncio

class ContASQLGetData4Bal(ContASQLMainClass, ConnASQLDataGet4Bal):
    def __init__(self):
        super().__init__()

async def main():
    req_dict = {
        'table_name': 'payments_in_table',
        'col_list': ['agent', 'sum', 'created'],
        'date_col': 'created',
        'from_date': '2023-06-01 00:00:00',
        'to_date': '2023-07-01 23:59:59',
        'factor': 1,
        'to_file': True,
    }
    tasks_list = list()
    tasks_list.append(controller.get_col_data_from_table_date_filtered_bal(**req_dict))

    req_dict['table_name'] = 'payments_out_table'
    req_dict['factor'] = -1
    tasks_list.append(controller.get_col_data_from_table_date_filtered_bal(**req_dict))

    req_dict['table_name'] = 'packlists_in_table'
    req_dict['factor'] = 1
    tasks_list.append(controller.get_col_data_from_table_date_filtered_bal(**req_dict))

    req_dict['table_name'] = 'packlists_out_table'
    req_dict['factor'] = -1
    tasks_list.append(controller.get_col_data_from_table_date_filtered_bal(**req_dict))

    req_dict['table_name'] = 'corr_bal_table'
    req_dict['factor'] = 1
    tasks_list.append(controller.get_col_data_from_table_date_filtered_bal(**req_dict))

    result = await asyncio.gather(*tasks_list)
    result_list = list()
    while result:
        l = result.pop()
        result_list.extend(l)
    result_list = sorted(result_list, key=lambda x: x[0])
    return result_list

if __name__ == '__main__':
    controller = ContASQLGetData4Bal()
    loop = asyncio.new_event_loop()
    data = loop.run_until_complete(main())
    print(data)
    print(len(data))

    # # loop.run_until_complete(connector.create_connection())
    # # loop.run_until_complete(connector.close_connection())
    # loop.run_until_complete(controller.get_table_data('pgsql_service_fields'))

