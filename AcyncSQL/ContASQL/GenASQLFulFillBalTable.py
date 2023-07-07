import datetime
import time
from AcyncSQL.ASQLMainClass import ASQLMainClass
import asyncio
import json

class GenASQLFulFillBalTable(ASQLMainClass):
    """ create table and makes customers_inn col from requested data"""
    excluded_inn_list = [None]
    daily_bal_table_name = 'customers_daily_bal_table'
    left_date = datetime.datetime(2021, 1, 1, 0, 0, 0)

    def __init__(self):
        super().__init__()


    async def put_data_to_daily_bal_table(self):
        # get current columns list
        from AcyncSQL.ContASQL.GenASQLCreateBalTable import GenASQLCreateBalTable
        gen_controller = GenASQLCreateBalTable()
        from AcyncSQL.ConnASQL.ConnASQLDataPut import ConnASQLDataPut
        gen_connector = ConnASQLDataPut()
        cur_inn_col_list = await gen_controller.request_cur_inn_col_list()
        cur_inn_col_list.remove('position_id')

        # creates working dictionary {inn_col: 0}
        cols_inn_val_dict = {inn: 0 for inn in cur_inn_col_list}
        cols_inn_val_dict.update({'bal_on_date': self.left_date.strftime('%Y-%m-%d %H:%M:%S')})

        # get transactions_list
        from AcyncSQL.ContASQL.ContASQLGetData4Bal import ContASQLGetData4Bal
        data_controller = ContASQLGetData4Bal()
        req_dict = {
            'from_date': self.left_date,
            'to_date': datetime.datetime.now(),
            # 'to_date': '2021-02-05 23:59:59.000',
        }
        transactions_list = await data_controller.get_list_inn_transactions_on_date(**req_dict)
        current_day = self.left_date
        current_day_start = current_day
        current_day_end = self.left_date + datetime.timedelta(days=1)
        print(current_day_start, current_day_end)

        for count, (transaction_date, cust_inn, transactions_sum) in enumerate(transactions_list):
            if cust_inn:   # filter None inn
                # waiting while transaction date will be near start date
                while transaction_date > current_day_end:
                    cols_inn_val_dict.update({'bal_on_date': current_day_end.strftime('%Y-%m-%d %H:%M:%S')})
                    # put data in table
                    req_dict = {
                        'table_name': 'customers_daily_bal_table',
                        'col_list': list(cols_inn_val_dict.keys()),  # form columns from work dict
                        'val_list': list(cols_inn_val_dict.values()),  # form values from work dict
                    }
                    await gen_connector.put_data_to_table_with_date(**req_dict)

                    # and up the current_date
                    current_day_start += datetime.timedelta(days=1)
                    current_day_end += datetime.timedelta(days=1)
                # if transaction date is proper - put data to main_dict
                current_cust_sum = cols_inn_val_dict.get(f"inn_{cust_inn}", 0)
                cols_inn_val_dict.update({f"inn_{cust_inn}": current_cust_sum + transactions_sum})
        # save last bal in file
        try:
            with open("customer_cur_bal_file.json", "w") as file:
                json.dump(cols_inn_val_dict, file)
        except Exception as e:
            print(f"cant_write file")
        return cols_inn_val_dict


if __name__ == '__main__':
    controller = GenASQLFulFillBalTable()
    loop = asyncio.new_event_loop()
    start_time = time.time()

    res = loop.run_until_complete(controller.put_data_to_daily_bal_table())
    print(f"daily bal table, returned value {res}")

    # res = loop.run_until_complete(controller.create_new_inn_col_daily_bal_table())
    # print(f"created table, returned value {res}")
    #
    # data = loop.run_until_complete(controller.request_cur_inn_col_list())
    # print(data)
    # print(f"number of columns {len(data)}")
    #
    # data = loop.run_until_complete(controller.request_inn_list())
    # print(data)
    # print(f"number of inns {len(data)}")
    #
    # data = loop.run_until_complete(controller.get_diff_col_inn())
    # print(data)
    # print(f"number of elements {len(data)}")

    loop.close()
    print(f"tasks finnished in {round(time.time() - start_time, 2)}sec")


