import psycopg2.errors

from PgsqlAlchemy.ModALUpdaters.ModALUpdaterMainClass import ModALUpdaterMainClass

from PgsqlAlchemy.ModAL.ModALBaseCustBal import ModALBaseCustBal
from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
from PgsqlAlchemy.ContMS.ContMSMain import ContMSMain

from sqlalchemy import create_engine, select, text, func
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import pandas as pd
import time
from tqdm import tqdm

__url = ConnALMainClass().get_url()
engine = create_engine(__url)

class ModALUpdCustBal(ModALUpdaterMainClass, ContMSMain, ModALBaseCustBal):
    model_name = "customers_bal_model"
    table_name = model_name
    model_config = None

    def __init__(self):
        super().__init__()
        self.logger = ModALUpdaterMainClass().logger
        self.logger.debug(f"{__class__.__name__} initialized")

    def update_cust_bal(self) -> dict:
        res_dict = dict({"table": self.table_name})
        from PgsqlAlchemy.ModALUpdaters.ModALGetTableData import ModALGetTableData
        data_to_update = ModALGetTableData().get_data_for_update_insertion(table_name=self.table_name)
        ans_dict = self.put_data_2table(list_of_dicts=data_to_update)
        res_dict.update(ans_dict)
        return res_dict

    def put_data_2table(self, list_of_dicts: list = None) -> dict:
        res_dict = dict({"inserted": 0, "updated": 0, "rows_requested": len(list_of_dicts), "rows_table": 0})
        ans_dict = dict()
        for i in tqdm(range(len(list_of_dicts))):
            ans_dict = self.insert_or_update_row_2table(list_of_dicts[i])
            res_dict["inserted"] = res_dict.get("inserted", 0) + ans_dict.get("inserted", 0)
            res_dict["updated"] = res_dict.get("updated", 0) + ans_dict.get("updated", 0)
        ans_dict = self.request_rows_num_in_table()
        res_dict["rows_table"] = ans_dict.get("table_rows", 0)
        self.logger.debug(f"{__class__.__name__} balance table inserted/updated {len(list_of_dicts)}rows")
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        eventer = ConnALEvent()
        event_dict = {
            "table_name": self.table_name,
            "description": f"inserted or updated {len(list_of_dicts)}rows in balance table",
            "event_from": "updater ModALFillCustBal",
        }
        eventer.put_event_2service_table_updates(**event_dict)
        return res_dict

    def insert_or_update_row_2table(self, row_dict: dict = None) -> dict:
        inserted_rows_num = 0
        updated_rows_num = 0
        try:
            new_cust_bal_row = ModALBaseCustBal(**row_dict)
            Session = sessionmaker(bind=engine)
            session = Session()
            # check is presence position?
            qry_object = session.query(ModALBaseCustBal).where(ModALBaseCustBal.counterparty == new_cust_bal_row.counterparty)
            if qry_object.first() is None:
                session.add(new_cust_bal_row)
                inserted_rows_num += 1
                # print(f"added client {new_cust_bal_row.counterparty.get('name')}")
            else:
                qry_object.update(row_dict)
                updated_rows_num += 1
                # print(f"updated client {new_cust_bal_row.counterparty.get('name')}")

            session.commit()


        except Exception as e:
            err_str = f"{__class__.__name__} balance table insertion interrupt, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"inserted": inserted_rows_num,
                     "updated": updated_rows_num})

    def request_rows_num_in_table(self):
        rows_in_table = 0
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            rows_in_table = session.query(func.count(ModALBaseCustBal.position_id)).scalar()
            session.commit()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table row counter interrupted, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"table_rows": rows_in_table})

if __name__ == '__main__':
    connector = ModALUpdCustBal()
    # connector.logger.info("testing ModALFillCustBal")
    # print(f"logger file name: {connector.logger_name}")
    # print(connector.get_last_update_date_from_service("customers_bal_table"))
    # print(connector.get_data_for_insertion("customers_bal_model"))
    start = time.time()
    print(connector.update_cust_bal())
    print(f"function time = {round(time.time() - start, 2)}sec")

