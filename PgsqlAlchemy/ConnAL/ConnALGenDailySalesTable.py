from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
import json
import ast

class ConnALGenDailySalesTable(ConnALMainClass):
    """ connector for generation daily report tables"""
    _engine = None
    __url = None

    def __init__(self):
        super().__init__()
        self.__url = self.get_url()

    def create_engine(self):
        try:
            self._engine = sqlalchemy.create_engine(self.__url, echo=True, pool_size=6, max_overflow=10)
            return True
        except Exception as e:
            print(e)
            self.logger.warning(f"{__class__.__name__} cant create new engine error: {e}")
            return False

    def get_all_tables_list(self):
        self.create_engine()
        inspector = sqlalchemy.inspect(self._engine)
        return inspector.get_table_names()

    def check_table_exist(self, table_name: str = None):
        self.create_engine()
        # res = self._engine.dialect.has_table(self._engine.connect(), table_name=table_name, schema='dbo')
        res = self._engine.dialect.has_table(connection=self._engine.connect(), table_name=table_name)
        return res

    def put_data_in_daily_sales_table(self, **kwargs):
        col_name = kwargs.get("col_name", None)
        data_list = kwargs.get("data_list", None)
        service_list = kwargs.get("service_list", None)
        model_class = kwargs.get("model_class", None)
        unique_col_name = kwargs.get("unique_col", None)
        # prepare customers counterparty and names dict {counterparty_meta: name}
        counterparty_names_dict = dict({str(cust.get("meta", None)): cust.get("name", None) for cust in service_list})

        # prepare data for insertion: customers counterparty sales dict {counterparty_meta: sum}
        counterparty_sales_sum_dict = dict()  # {counterparty_meta: sales_sum}
        stores_sum_dict = dict()  # {store_meta: store_sum}
        for demand in data_list:
            # get counterparty_meta
            counterparty = demand.get("agent", None)["meta"]
            counterparty_str = str(counterparty)
            new_dict = {counterparty_str: counterparty_sales_sum_dict.get(counterparty_str, 0) + demand.get("sum", 0)/100}
            counterparty_sales_sum_dict.update(new_dict)

        inserted_rows_num = 0
        updated_rows_num = 0
        today = datetime.datetime.now()
        try:
            self.create_engine()

            for counterparty_str, sales_sum in counterparty_sales_sum_dict.items():
                counterparty = ast.literal_eval(counterparty_str)
                counterparty_name = counterparty_names_dict.get(counterparty_str, None)
                row_dict = dict({"counterparty": counterparty,
                                 "update": today,
                                 col_name:  sales_sum,
                                 "name": counterparty_name})
                new_model_obj = model_class(**row_dict)
                Session = sessionmaker(bind=self._engine)
                session = Session()
                # check is presence position?
                qry_object = session.query(model_class).where(getattr(model_class, unique_col_name) == getattr(new_model_obj, unique_col_name))

                if qry_object.first() is None:
                    session.add(new_model_obj)
                    inserted_rows_num += 1
                    # print(f"added client {new_cust_bal_row.counterparty.get('name')}")
                else:
                    qry_object.update(row_dict)
                    updated_rows_num += 1
                    # print(f"updated client {new_cust_bal_row.counterparty.get('name')}")
                session.commit()

        except Exception as e:
            err_str = f"{__class__.__name__} balance table insertion interrupt, error: {e}"
            print(err_str)
            self.logger.error(err_str)

        return dict({"inserted": inserted_rows_num, "updated": updated_rows_num})



if __name__ == '__main__':
    connector = ConnALGenDailySalesTable()
    # print(connector.create_engine())
    # print(connector.get_all_tables_list())
    print(connector.check_table_exist("invin_model"))