import datetime
import time
from AcyncSQL.ASQLMainClass import ASQLMainClass

import asyncio


class GenASQLCreateBalTable(ASQLMainClass):
    """ create table and makes customers_inn col from requested data"""
    excluded_inn_list = [None]
    daily_bal_table_name = 'customers_daily_bal_table'

    def __init__(self):
        super().__init__()

    async def create_empty_daily_bal_table_and_base_cols(self):
        """ only creates table with three columns"""
        table_name = self.daily_bal_table_name
        from AcyncSQL.ConnASQL.ConnASQLCreate import ConnASQLCreate
        conector = ConnASQLCreate()
        result = await conector.create_table_with_position_id(table_name=table_name)
        req_dict = {
            'table_name': 'customers_daily_bal_table',
            'col_name': 'bal_on_date',
            'col_type': 'TIMESTAMP',
        }
        await conector.create_col_in_table(**req_dict)
        req_dict = {
            'table_name': 'customers_daily_bal_table',
            'col_name': 'bal_on_date',
        }
        await conector.mark_unique_col_in_table(**req_dict)
        return result

    async def create_new_inn_col_daily_bal_table(self):
        """ requests all inn not presence in table and creates them"""
        table_name = self.daily_bal_table_name
        list_new_inn_cols = await self.get_diff_col_inn()
        from AcyncSQL.ConnASQL.ConnASQLCreate import ConnASQLCreate
        connector = ConnASQLCreate()
        for new_col_name in list_new_inn_cols:
            req_dict = {
                'table_name': table_name,
                'col_name': new_col_name,
                'col_type': 'DOUBLE PRECISION',
                'col_default': 0
            }
            await connector.create_col_in_table_with_default(**req_dict)
        return True

    async def create_new_id_col_daily_bal_table(self):
        """ requests all id not presence in table and creates them"""
        table_name = self.daily_bal_table_name
        list_new_inn_cols = await self.get_diff_col_id()
        from AcyncSQL.ConnASQL.ConnASQLCreate import ConnASQLCreate
        connector = ConnASQLCreate()
        for new_col_name in list_new_inn_cols:
            req_dict = {
                'table_name': table_name,
                'col_name': new_col_name,
                'col_type': 'DOUBLE PRECISION',
                'col_default': 0
            }
            await connector.create_col_in_table_with_default(**req_dict)
        return True

    async def request_cur_inn_col_list(self) -> list:
        """ return list of current inn columns in daily_balance"""
        table_name = self.daily_bal_table_name
        from AcyncSQL.ConnASQL.ConnASQLColGet import ConnASQLDataGet
        col_inn_list = await ConnASQLDataGet().get_table_col_names(table_name=table_name)
        return col_inn_list

    async def request_cur_id_col_list(self) -> list:
        """ return list of current inn columns in daily_balance"""
        table_name = self.daily_bal_table_name
        from AcyncSQL.ConnASQL.ConnASQLColGet import ConnASQLDataGet
        col_id_list = await ConnASQLDataGet().get_table_col_names(table_name=table_name)
        return col_id_list

    async def request_inn_list(self) -> list:
        """ return list of inn from customers_table"""
        table_name = 'customers_table'
        from AcyncSQL.ConnASQL.ConnASQLDataGet import ConnASQLDataGet
        pd_data = await ConnASQLDataGet().get_col_data_from_table_pd(table_name=table_name, col_list=['inn'])
        inn_list = [inn for inn in pd_data["inn"] if inn not in self.excluded_inn_list]
        return list(set(inn_list))

    async def request_id_list(self) -> list:
        """ return list of id from customers_table"""
        table_name = 'customers_table'
        from AcyncSQL.ConnASQL.ConnASQLDataGet import ConnASQLDataGet
        pd_data = await ConnASQLDataGet().get_col_data_from_table_pd(table_name=table_name, col_list=['id'])
        id_list = [cust_id for cust_id in pd_data["id"] if cust_id not in self.excluded_inn_list]
        return list(set(id_list))

    async def get_diff_col_inn(self) -> list:
        """ compare inn_col and inn from customer_table and
        return differences_list"""
        diff_list = list()
        col_list = await self.request_cur_inn_col_list()
        inn_list = await self.request_inn_list()
        for inn in inn_list:
            col_name = f"inn_{inn}"
            if col_name not in col_list:
                diff_list.append(col_name)
        return diff_list

    async def get_diff_col_id(self) -> list:
        """ compare inn_col and inn from customer_table and
        return differences_list"""
        diff_list = list()
        col_list = await self.request_cur_id_col_list()
        id_list = await self.request_id_list()
        for id in id_list:
            col_name = f"uid_{id}"
            if col_name not in col_list:
                diff_list.append(col_name)
        return diff_list

def main():
    controller = GenASQLCreateBalTable()
    loop = asyncio.new_event_loop()
    start_time = time.time()

    res = loop.run_until_complete(controller.create_empty_daily_bal_table_and_base_cols())
    print(f"created table, returned value {res}")

    res = loop.run_until_complete(controller.create_new_inn_col_daily_bal_table())
    print(f"created table, returned value {res}")

    loop.close()
    print(f"tasks finnished in {round(time.time() - start_time, 2)}sec")


if __name__ == '__main__':
    main()
    # controller = GenASQLCreateBalTable()
    # loop = asyncio.new_event_loop()
    # start_time = time.time()
    #
    # res = loop.run_until_complete(controller.get_diff_col_id())
    # print(f"created table, returned value {res}")
    #
    # loop.close()
    # print(f"tasks finnished in {round(time.time() - start_time, 2)}sec")



