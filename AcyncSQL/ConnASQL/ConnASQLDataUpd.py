import datetime

from AcyncSQL.ConnASQL.ConnASQLMainClass import ConnASQLMainClass
import pandas as pd
import asyncio
import asyncpg
import json
import re


class ConnASQLDataUpd(ConnASQLMainClass):
    _conn = None
    __config_dict = dict()
    left_date = datetime.datetime(2018, 1, 1)

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

    async def check_record_json(self, **kwargs):
        """ is string presence in table if not -> insert it"""
        req_data = {
            "table_name": kwargs.get("table_name", None),
            "col_name": kwargs.get("col_name", None),
            "col_val": kwargs.get("col_val", None),
        }
        from AcyncSQL.ConnASQL.ConnASQLDataGet import ConnASQLDataGet
        pd_data = await ConnASQLDataGet().get_row_from_table_pd_json(**req_data)
        return pd_data

    async def upd_data_in_table(self, **kwargs) -> dict:
        table_name = kwargs.get('table_name', None)
        unique_dict = kwargs.get('unique_dict', None)
        col_list = kwargs.get('col_list', None)
        val_list = kwargs.get('val_list', None)
        _conn = await asyncpg.connect(**self.__config_dict)
        col_val_str = await self.value_str_handler(col_list=col_list, val_list=val_list)
        unique_str = await self.unique_str_handler(unique_dict=unique_dict)
        req_line = f"UPDATE {table_name} SET {col_val_str} WHERE {unique_str};"
        await _conn.fetch(req_line)
        await _conn.close()
        return True

    async def value_str_handler(self, col_list: list = None, val_list: list = None, **kwargs) -> str:
        result_str_list = list()
        if len(col_list) == len(val_list):
            for i, col_name in enumerate(col_list):
                col_val_str = f" {col_name} = {val_list[i]}"
                result_str_list.append(col_val_str)
        result_str = ", ".join(result_str_list)
        return result_str

    async def unique_str_handler(self, unique_dict: dict = None) -> str:
        # from https://popsql.com/learn-sql/postgresql/how-to-query-a-json-column-in-postgresql
        result_str = str()
        col_type = unique_dict.get("type")
        col_name = unique_dict.get("unique_col_name")
        col_tag = unique_dict.get("tag")
        col_val = unique_dict.get("unique_val")
        if col_type == "JSON":
            real_value = col_val.get(col_tag, None)
            result_str = f"{col_name} ->> '{col_tag}' = '{real_value}'"
        else:
            result_str = f"{col_name} = {col_val}"

        return result_str


if __name__ == '__main__':
    connector = ConnASQLDataUpd()
    loop = asyncio.new_event_loop()
    req_dict = {"table_name": "customers_bal_table",
                "unique_dict": {"type": "JSON",
                                "unique_col_name": "counterparty",
                                "tag": "id",
                                "unique_val": {"meta":
                                                   {"href":
                                                        "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/02a517d3-a78b-11ed-0a80-10870008fd53",
                                                    "metadataHref": "https://online.moysklad.ru/api/remap/1.2/entity/counterparty/metadata",
                                                    "type": "counterparty", "mediaType": "application/json",
                                                    "uuidHref": "https://online.moysklad.ru/app/#company/edit?id=02a517d3-a78b-11ed-0a80-10870008fd53"},
                                               "id": "02a517d3-a78b-11ed-0a80-10870008fd53",
                                               "name": "ООО АСК",
                                               "externalCode": "GrQQb4tzggfccJy3866zF2",
                                               "email": "info@ask66.ru",
                                               "phone": "+7 (343) 289-21-82",
                                               "inn": "6678000288",
                                               "companyType": "legal"}},
                "col_list": ["balance", "profit"],
                "val_list": [0.0, 0.0]}
    task1 = connector.upd_data_in_table(**req_dict)

    data = loop.run_until_complete(task1)
    loop.close()
    print(data)
    print("finish")
