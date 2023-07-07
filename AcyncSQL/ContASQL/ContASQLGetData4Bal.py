from AcyncSQL.ContASQL.ContASQLMainClass import ContASQLMainClass
from AcyncSQL.ConnASQL.ConnASQLDataGet4Bal import ConnASQLDataGet4Bal
import asyncio
import datetime


class ContASQLGetData4Bal(ContASQLMainClass, ConnASQLDataGet4Bal):
    def __init__(self):
        super().__init__()

    async def get_list_inn_transactions_on_date(self, **kwargs):
        req_dict1 = {
            'from_date': kwargs.get('from_date', self.left_date),
            'to_date': kwargs.get('to_date', datetime.datetime.now()),
            'to_file': True,
        }

        # request inn dictionary
        req_dict2 = {
            'table_name': 'customers_table',
            'col_list': ['meta', 'inn'],
            'to_file': True,
        }

        transaction_list = await self.get_transactions_list_on_date(**req_dict1)
        href_dict = await self.get_col_data_from_table_inn(**req_dict2)
        print(f"number of transactions {len(transaction_list)}")
        result_list = [(tr_date, href_dict.get(href, None), tr_sum) for tr_date, href, tr_sum in transaction_list]
        # result_list_sorted = sorted(result_list, key=lambda x: x[0])

        return result_list

    async def get_transactions_list_on_date(self, **kwargs):
        req_dict = {
            'table_name': 'payments_in_table',
            'col_list': ['agent', 'sum', 'created'],
            'date_col': 'created',
            'from_date': kwargs.get('from_date', self.left_date),
            'to_date': kwargs.get('to_date', datetime.datetime.now()),
            'factor': 1,
            'to_file': True,
        }
        tasks_list = list()
        tasks_list.append(self.get_col_data_from_table_date_filtered_bal(**req_dict))

        req_dict['table_name'] = 'payments_out_table'
        req_dict['factor'] = -1
        tasks_list.append(self.get_col_data_from_table_date_filtered_bal(**req_dict))

        req_dict['table_name'] = 'packlists_in_table'
        req_dict['factor'] = 1
        tasks_list.append(self.get_col_data_from_table_date_filtered_bal(**req_dict))

        req_dict['table_name'] = 'packlists_out_table'
        req_dict['factor'] = -1
        tasks_list.append(self.get_col_data_from_table_date_filtered_bal(**req_dict))

        req_dict['table_name'] = 'corr_bal_table'
        req_dict['factor'] = 1
        tasks_list.append(self.get_col_data_from_table_date_filtered_bal(**req_dict))

        # get data from tables to req_result
        req_result = await asyncio.gather(*tasks_list)
        result_list = list()
        while req_result:
            transaction_result_list = req_result.pop()
            result_list.extend(transaction_result_list)
        #sorting list
        result_list = sorted(result_list, key=lambda x: x[0])
        return result_list


if __name__ == '__main__':
    controller = ContASQLGetData4Bal()
    loop = asyncio.new_event_loop()
    req_dict = {
        'from_date': '2018-07-07 00:00:00.000',
        'to_date': '2021-02-05 23:59:59.000',
        'to_file': True,
    }
    data = loop.run_until_complete(controller.get_list_inn_transactions_on_date(**req_dict))
    loop.close()
    print(data)
    print(f"number of transactions {len(data)}")

    # # loop.run_until_complete(connector.create_connection())
    # # loop.run_until_complete(connector.close_connection())
    # loop.run_until_complete(controller.get_table_data('pgsql_service_fields'))
