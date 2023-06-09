from AcyncSQL.ASQLMainClass import ASQLMainClass
import asyncio
import time
import json

class GenASQLUpdDailyBal(ASQLMainClass):
    daily_bal_table_name = 'customers_daily_bal_table'
    def __init__(self):
        super().__init__()

    async def check_cur_bal_with_table(self):
        """ create dictionary with inn and correction sum for daily cust balance"""
        table_name = self.daily_bal_table_name
        from AcyncSQL.ConnASQL.ConnASQLDataGet4Bal import ConnASQLDataGet4Bal
        bal_connector = ConnASQLDataGet4Bal()
        # get last row in table customer_daily_bal
        daily_table_dict = await bal_connector.get_last_row_in_table_pd(table_name=table_name)

        # request data from customers_balance and convert to dict {uid: bal}
        req_dict = {
            'table_name': 'customers_bal_table',
            'col_list': ['meta', 'balance'],
        }
        bal_table_pd = await bal_connector.get_col_data_from_table(**req_dict)
        href_bal_list = bal_table_pd.values.tolist()
        href_bal_dict = dict({str(href_str.split("/")[8]).split('"')[0]: bal/100 for href_str, bal in href_bal_list})

        # request data from customers_table and convert to dict {uid: inn}
        req_dict2 = {
            'table_name': 'customers_table',
            'col_list': ['id', 'inn'],
        }
        cust_table_pd = await bal_connector.get_col_data_from_table(**req_dict2)
        href_inn_list = cust_table_pd.values.tolist()
        href_inn_dict = dict({str(cust_id): inn_str for cust_id, inn_str in href_inn_list})

        # make dict {col_inn: bal}
        col_inn_bal_dict = {f"inn_{href_inn_dict.get(cust_id, 'unknown')}": bal for cust_id, bal in href_bal_dict.items() if cust_id}

        # main loop
        correction_dict = dict({'corr_date': '2023-07-07 23:59:59'})
        for inn, bal in col_inn_bal_dict.items():
            daily_table_bal = daily_table_dict.get(inn, 0)
            daily_table_bal = round(daily_table_bal, 2)
            delta = round(bal - daily_table_bal)
            if max(delta, -delta) > 1:
                correction_dict.update({inn.split('_')[-1]: delta})
                print(f"for inn {inn.split('_')[-1]} table_bal={daily_table_bal} vs real_bal={bal}")
                # save last bal in file
        try:
            with open("corr_bal_sum.json", "w") as file:
                json.dump(correction_dict, file)
        except Exception as e:
            print(f"cant_write file, error: {e}")
        return correction_dict



def main():
    controller = GenASQLUpdDailyBal()
    loop = asyncio.new_event_loop()
    start_time = time.time()

    res = loop.run_until_complete(controller.check_cur_bal_with_table())
    print(f"created table, returned value {res}")

    # res = loop.run_until_complete(controller.create_new_inn_col_daily_bal_table())
    # print(f"created table, returned value {res}")

    loop.close()
    print(f"tasks finnished in {round(time.time() - start_time, 2)}sec")


if __name__ == '__main__':
    main()