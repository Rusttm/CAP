import psycopg2.errors

from PgsqlAlchemy.ModALFillers.ModALFillerMainClass import ModALFillerMainClass
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

class ModALFillCustBal(ModALFillerMainClass, ModALBaseCustBal, ContMSMain):
    model_name = "customers_bal_model"
    table_name = model_name
    model_config = None

    def __init__(self):
        super().__init__()
        self.logger = ModALFillerMainClass().logger
        self.logger.debug(f"{__class__.__name__} initialized")

    def update_cust_bal(self):
        data_to_update = self.get_data_for_insertion(table_name=self.table_name)
        self.put_data_2table(list_of_dicts=data_to_update)
    def get_data_for_insertion(self, table_name: str = table_name) -> list:
        """ gets MSMain function from model table and run/get data for insertion"""
        if table_name:
            self.table_name = table_name
        # gets functon name from config
        from PgsqlAlchemy.ConnMS.ConnMSReadJson import ConnMSReadJson
        self.model_config = ConnMSReadJson().get_config_json_data(file_name=self.table_name)
        table_data_function = self.model_config.get("ms_func", None)

        # make connector to service event table
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        service_event = ConnALEvent()
        # run function
        from PgsqlAlchemy.ContMS.ContMSMain import ContMSMain
        ms_controller = ContMSMain()
        request_func = getattr(ms_controller, table_data_function)
        try:
            # request last date of updated data
            from_date = service_event.get_last_update_date_from_service(event_table=self.table_name)
        except Exception as e:
            # self.logger.error(f"{__class__.__name__} cant get last data update, error: {e}")
            from_date = datetime.datetime(2018, 1, 1, 0, 0, 0).strftime("%Y-%m-%d %H:%M:%S")
        to_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"requested customers balances: {from_date=} / {to_date=}")
        req_data = request_func(from_date=from_date, to_date=to_date)
        return req_data

    def put_data_2table(self, list_of_dicts: list = None):
        for i in tqdm(range(len(list_of_dicts))):
            self.insert_or_update_row_2table(list_of_dicts[i])
        self.logger.debug(f"{__class__.__name__} balance table inserted/updated {len(list_of_dicts)}rows")
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        eventer = ConnALEvent()
        event_dict = {
            "table_name": self.table_name,
            "description": f"inserted or updated {len(list_of_dicts)}rows in balance table",
            "event_from": "updater ModALFillCustBal",
        }
        eventer.put_event_2service_table_updates(**event_dict)

    def insert_or_update_row_2table(self, row_dict: dict = None):
        try:
            new_cust_bal_row = ModALBaseCustBal(**row_dict)
            Session = sessionmaker(bind=engine)
            session = Session()
            # check is presence position?
            qry_object = session.query(ModALBaseCustBal).where(ModALBaseCustBal.counterparty == new_cust_bal_row.counterparty)
            if qry_object.first() is None:
                session.add(new_cust_bal_row)
                # print(f"added client {new_cust_bal_row.counterparty.get('name')}")
            else:
                qry_object.update(row_dict)
                # print(f"updated client {new_cust_bal_row.counterparty.get('name')}")
            session.commit()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table insertion interrupt, error {e}"
            print(err_str)
            self.logger.error(err_str)


if __name__ == '__main__':
    connector = ModALFillCustBal()
    # connector.logger.info("testing ModALFillCustBal")
    # print(f"logger file name: {connector.logger_name}")
    # print(connector.get_last_update_date_from_service("customers_bal_table"))
    # print(connector.get_data_for_insertion("customers_bal_model"))
    start = time.time()
    print(connector.update_cust_bal())
    print(f"function time = {round(time.time() - start, 2)}sec")

