from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
import sqlalchemy
import datetime
from sqlalchemy.orm import sessionmaker
import json
import ast

class ConnALGenDailyStockStoreTable(ConnALMainClass):
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

    def put_data_in_daily_stock_store_table(self, **kwargs):
        col_name = kwargs.get("col_name", None)
        data_list = kwargs.get("data_list", None)
        service_list = kwargs.get("service_list", None)
        model_class = kwargs.get("model_class", None)
        unique_col_name = kwargs.get("unique_col", None)
        # prepare prod dict {meta: price}
        prod_price_dict = dict({str(prod.get("meta", None)): prod.get("price", None)/100 for prod in service_list})

        # prepare data for insertion: format table from products by store on store
        stores_names_dict = dict()
        stores_sum_dict = dict()
        for prod in data_list:
            prod_meta = prod.get("meta", None)
            for store in prod.get("stockByStore", None):
                store_meta = store.get("meta", None)
                store_name = store.get("name", None)
                store_stock = store.get("stock", None)
                store_prod_sum = prod_price_dict.get(str(prod_meta), 0) * store_stock
                stores_names_dict.update({str(store_meta): store_name})
                stores_sum_dict[str(store_meta)] = stores_sum_dict.get(str(store_meta), 0) + store_prod_sum


        inserted_rows_num = 0
        updated_rows_num = 0
        today = datetime.datetime.now()
        # unique_col_name = "counterparty"
        try:
            self.create_engine()

            for store_str, store_sum in stores_sum_dict.items():
                # store_dict = json.loads(store_str)
                store_dict = ast.literal_eval(store_str)
                store_name = stores_names_dict.get(store_str, None)
                row_dict = dict({"store": store_dict,
                                 "update": today,
                                 col_name:  store_sum,
                                 "name": store_name})
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
    connector = ConnALGenDailyStockStoreTable()
    # print(connector.create_engine())
    # print(connector.get_all_tables_list())
    print(connector.check_table_exist("invin_model"))