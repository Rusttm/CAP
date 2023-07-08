from AcyncSQL.ASQLMainClass import ASQLMainClass


import asyncio
import time
import json
import datetime
from tqdm import tqdm

class ASQLUpdater(ASQLMainClass):
    def __init__(self):
        super().__init__()
        from AcyncSQL.ConnASQL.ConnASQLJsonConfig import ConnASQLJsonConfig
        self.tables_config = ConnASQLJsonConfig().get_tables_config()

    def non_async_daily_bal_updater(self):
        controller = ASQLUpdater()
        start_time = time.time()
        res = loop.run_until_complete(controller.customer_daily_bal_table_updater())
        del res["bal_on_date"]
        res_bal_sum = 0
        try:
            for bal in res.values():
                res_bal_sum += bal
        except Exception as e:
            error_str = f"cant count summary balance, error: {e}"
            print(error_str)
            self.logger.error(error_str)
        loop.close()
        res_str = f"table 'customer_daily_bal' updated summary balance = {res_bal_sum} \n"
        res_str += f" task finished in {round(time.time() - start_time, 2)}sec"

        return res_str

    def non_async_daily_updater(self) -> str:
        from API_MS.MSMain import MSMain
        ms_connector = MSMain()
        from AcyncSQL.ConnASQL.ConnASQLRowCount import ConnASQLRowCount
        row_counter = ConnASQLRowCount()
        from AcyncSQL.ConnASQL.ConnASQLDataUpd import ConnASQLDataUpd
        upd_connector = ConnASQLDataUpd()

        async_tasks_list = []
        for table_name, data_dict in self.tables_config.items():
            # skip non updated tables
            if data_dict.get('sql_upd', None) != 1:
                continue
            # in second get function from MS controllers in MsMain
            table_data_function = data_dict.get('function', None)
            if not table_data_function:
                continue

            # start main loop
            gen_start = time.time()
            # gets data list from MS module
            request_func = getattr(ms_connector, table_data_function)
            req_data = request_func()
            data_list = req_data.get('data', [])

            unique_dict = data_dict.get('unique', None)
            upd_col_list = data_dict.get('upd_cols', None)
            # rows_in_table = row_counter.non_async_get_table_row_num(table_name=table_name)
            rows_in_table = asyncio.run(row_counter.get_table_row_num(table_name=table_name))
            # from https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait
            # from https://stackoverflow.com/questions/73361664/asyncio-get-event-loop-deprecationwarning-there-is-no-current-event-loop
            # loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(loop)
            rows_in_request = len(data_list)
            for i in tqdm(range(rows_in_request)):
                row_dict = dict(data_list[i])
                # put in unique dictionary col value
                unique_col_name = unique_dict.get("unique_col_name", None)
                unique_col_val = row_dict.pop(unique_col_name)
                unique_dict.update({"unique_val": unique_col_val})
                val_list = [row_dict.get(col_name, None) for col_name in upd_col_list]
                req_dict = {
                    'table_name': table_name,
                    'unique_dict': unique_dict,
                    'col_list': upd_col_list,
                    'val_list': val_list
                }

                asyncio.run(upd_connector.upd_data_in_table(**req_dict))
                # async_tasks_list.append(upd_connector.upd_data_in_table(**req_dict))
            # tasks_group = asyncio.gather(*async_tasks_list)
            # loop.run_until_complete(tasks_group)
            # loop.close()
            end = time.time()
            res_string = f"table: {table_name} ({rows_in_table}rows from {len(data_list)}) updated in {round(end - gen_start, 2)}sec\n"
            print(res_string)

        return res_string


if __name__ == '__main__':
    controller = ASQLUpdater()
    controller.non_async_daily_updater()