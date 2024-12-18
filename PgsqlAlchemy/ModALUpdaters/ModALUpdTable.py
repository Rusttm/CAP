# import psycopg2.errors

from PgsqlAlchemy.ModALUpdaters.ModALUpdaterMainClass import ModALUpdaterMainClass

from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
from PgsqlAlchemy.ContMS.ContMSMain import ContMSMain

from sqlalchemy import create_engine, select, text, func
# from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.orm import scoped_session, sessionmaker
# import datetime
# import pandas as pd
import time
from tqdm import tqdm
import importlib

__url = ConnALMainClass().get_url()
engine = create_engine(__url)

class ModALUpdTable(ModALUpdaterMainClass, ContMSMain):
    """ insert or update data in table"""
    # model_name = "customers_bal_model"
    # table_name = model_name
    model_config = None
    models_module = "PgsqlAlchemy.ModAL"

    def __init__(self):
        super().__init__()
        self.logger = ModALUpdaterMainClass().logger
        self.logger.debug(f"{__class__.__name__} initialized")

    def update_model_table(self, model_class_name: str = None,
                           model_unique_col: str = None,
                           model_class_table: str = None) -> dict:
        """ main updater for MS_API data:
         1. gets data from MS API
         2. put/update data in table
         3. write to service table
         4. return dict {"inserted": 0, "updated": 0, "rows_requested": len(list_of_dicts), "rows_table": 0}"""
        res_dict = dict({"table": model_class_table})
        from PgsqlAlchemy.ModALUpdaters.ModALGetTableData import ModALGetTableData
        # data from MS_API that depends on service table
        data_to_update = ModALGetTableData().get_data_for_update_insertion(table_name=model_class_table)

        # make model class from string 'model_class'
        module_str = f"{self.models_module}.{model_class_name}"
        module = importlib.import_module(module_str)
        # create model class (not obj)
        model_class = getattr(module, model_class_name)
        # model_unique_col = "counterparty"
        # send class to putter for creation class_obj
        ans_dict = self.put_data_2table(list_of_dicts=data_to_update,
                                        model_class=model_class,
                                        model_unique_col=model_unique_col,
                                        model_class_table=model_class_table)
        # update service table
        res_dict.update(ans_dict)
        return res_dict

    def put_data_2table(self, list_of_dicts: list = None,
                        model_class: object = None,
                        model_unique_col: str = None,
                        model_class_table: str = None) -> dict:
        """ general function to put data in table by sqlAlchemy
        list_of_dicts - [{'col_name1': col1_value}, {'col_name2': col2_value}]
        model_class_table -name of table
        model_class - class model (class as obj)
        unique_col - used to check current presence"""
        # check the data dict {'col_name': col_value}
        if not list_of_dicts:
            err_str = f"{__class__.__name__} cant get information for update {model_class_table} from MoiSklad"
            print(err_str)
            self.logger.error(err_str)
            list_of_dicts = []
        res_dict = dict({"inserted": 0, "updated": 0, "rows_requested": len(list_of_dicts), "rows_table": 0})

        ans_dict = dict()
        start_time = time.time()
        print(f"updating {model_class_table}")
        for i in tqdm(range(len(list_of_dicts))):
        # for i in range(len(list_of_dicts)):
            ans_dict = self.insert_or_update_row_2table(list_of_dicts[i], model_class, model_unique_col)
            res_dict["inserted"] = res_dict.get("inserted", 0) + ans_dict.get("inserted", 0)
            res_dict["updated"] = res_dict.get("updated", 0) + ans_dict.get("updated", 0)

        # get number of rows in current table
        ans_dict = self.request_rows_num_in_table(model_class=model_class)
        res_dict["rows_table"] = ans_dict.get("table_rows", 0)
        debug_str = f"{__class__.__name__} model {model_class} table inserted/updated {len(list_of_dicts)}rows by {model_unique_col}"
        self.logger.debug(debug_str)
        debug_str = f"{__class__.__name__} table {model_class_table} updated in {round(time.time() - start_time, 2)}sec\n"
        print(debug_str)
        self.logger.debug(debug_str)

        # update service table events
        from PgsqlAlchemy.ConnAL.ConnALEvent import ConnALEvent
        eventer = ConnALEvent()
        event_dict = {
            "table_name": model_class_table,
            "description": f"inserted or updated {len(list_of_dicts)}rows in balance table",
            "event_from": f"updater {__class__.__name__}",
        }
        eventer.put_event_2service_table_updates(**event_dict)
        eventer.clear_old_records_from_event_table(table_name=model_class_table)

        return res_dict

    def insert_or_update_row_2table(self,
                                    row_dict: dict = None,
                                    model_class: object = None,
                                    unique_col_name: str = None) -> dict:
        """ base function that works with table"""
        inserted_rows_num = 0
        updated_rows_num = 0
        try:
            # new_cust_bal_row = ModALBaseCustBal(**row_dict)
            # create class object
            new_model_obj = model_class(**row_dict)
            Session = sessionmaker(bind=engine)
            session = Session()
            # check is presence position with unique_col
            qry_object = session.query(model_class).where(getattr(model_class,unique_col_name) == getattr(new_model_obj,unique_col_name))
            # insert row
            if qry_object.first() is None:
                session.add(new_model_obj)
                inserted_rows_num += 1
                # print(f"added client {new_cust_bal_row.counterparty.get('name')}")
            # or update row
            else:
                qry_object.update(row_dict)
                updated_rows_num += 1
                # print(f"updated client {new_cust_bal_row.counterparty.get('name')}")

            session.commit()


        except Exception as e:
            err_str = f"{__class__.__name__} profit table insertion interrupt, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"inserted": inserted_rows_num,
                     "updated": updated_rows_num})

    def request_rows_num_in_table(self, model_class: object = None ):
        """ gets row number in current table
        returns dict {'table_rows': num_of_rows}"""
        rows_in_table = 0
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
            rows_in_table = session.query(func.count(getattr(model_class, "position_id"))).scalar()
            session.commit()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table row counter interrupted, error {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"table_rows": rows_in_table})

if __name__ == '__main__':
    connector = ModALUpdTable()
    # connector.logger.info("testing ModALFillCustBal")
    # print(f"logger file name: {connector.logger_name}")
    # print(connector.get_last_update_date_from_service("customers_bal_table"))
    # print(connector.get_data_for_insertion("customers_bal_model"))
    # start = time.time()
    # print(connector.update_cust_bal())
    # print(f"function time = {round(time.time() - start, 2)}sec")

