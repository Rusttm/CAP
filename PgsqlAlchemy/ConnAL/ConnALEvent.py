from PgsqlAlchemy.ModALUpdaters.ModALUpdaterMainClass import ModALUpdaterMainClass
import datetime
from PgsqlAlchemy.ModAL.ModALBaseService import ModALBaseService
from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
from PgsqlAlchemy.ContMS.ContMSMain import ContMSMain

from sqlalchemy import create_engine, select, text, func, delete
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import pandas as pd

__url = ConnALMainClass().get_url()
engine = create_engine(__url)


class ConnALEvent(ConnALMainClass, ModALBaseService):

    def __init__(self):
        super().__init__()

    def put_event_2service_table_updates(self, **kwargs):
        table_name: str = None
        description: str = None
        event_from: str = None
        from_date: datetime = None,
        to_date: datetime = None
        """ put in service table information about updates of tables"""
        now_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_dict = {"event_name": "table_updated",
                      "event_descr": f"new updates in table {kwargs.get('table_name', 'unknown')}: {kwargs.get('description', 'no descr')}",
                      # "event_to": "telegram",
                      "event_from": kwargs.get("event_from", "updater"),
                      # "event_level": 10,
                      # "event_active": False,
                      "event_table": kwargs.get("table_name", "unknown"),
                      "event_time": now_string,
                      "event_period_start": kwargs.get("from_date", now_string),
                      "event_period_end": kwargs.get("to_date", now_string)
                      }

        # new_event_row = ModALBaseService.py(**event_dict)

        try:
            # version1 works
            # DBSession = scoped_session(sessionmaker(bind=engine))
            # DBSession.bulk_insert_mappings(ModALBaseService, [event_dict])
            # DBSession.commit()

            # version2 doesnt insert but increase autoincrement
            # ins = insert(ModALBaseService).values(event_dict)
            # with engine.connect() as conn:
            #     conn.execute(ins)
            #     print(ins.returning(ModALBaseService.event_descr))

            # version3 works
            session = sessionmaker(bind=engine)()
            new_model_obj = ModALBaseService(**event_dict)
            res = session.merge(new_model_obj)
            session.commit()
            # print(res.event_descr)
            self.logger.debug(f"{__class__.__name__} event table updated: {event_dict.get('event_descr')}")

            return True

        except Exception as e:
            error_str = f"service table was not updated with table {table_name}, error: {e}"
            # print(error_str)
            self.logger.error(error_str)
            return False

    def get_last_update_date_from_service(self, event_table: str = None) -> datetime:
        """ return minimal date of update table"""
        from PgsqlAlchemy.ModAL.ModALBaseService import ModALBaseService

        req_line = f"SELECT event_table, event_from, MAX(event_time), MAX (event_period_end) " \
                   f"FROM pgsql_service " \
                   f"WHERE event_table='{event_table}' AND event_from='updater' " \
                   f"GROUP BY event_table, event_from"
        if event_table:
            try:
                t = ModALBaseService

                # version0
                conn = engine.connect()
                selector = select(t.event_table, t.event_from, func.max(t.event_time), func.max(t.event_period_end))
                after_where = selector.where(t.event_table == event_table and t.event_from == "updater")
                after_grouper = after_where.group_by(t.event_table, t.event_from)
                s = after_grouper
                # variant0_1
                # ans = conn.execute(s)
                # for row in ans:
                #     print(row)
                # variant0_2
                df = pd.read_sql(s, con=conn)
                if df.empty:
                    result = datetime.datetime(2018, 1, 1, 0, 0, 0)
                else:
                    result = min(df['max_1'].iloc[0], df['max_2'].iloc[0])
                return result

                # version1
                # with engine.connect() as con:
                #     ans = con.execute(text(req_line))
                # for row in ans:
                #     print(row)

                # version2
                # s = select(t.event_table, t.event_from).where(t.event_table == event_table)
                # with engine.connect() as conn:
                #     for row in conn.execute(s):
                #         print(row)

            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} error while request last update date {event_table}: {e}")
        else:
            self.logger.warning(f"{__class__.__name__} request not specified event_table_name={event_table}")
            self.logger.info(f"{__class__.__name__} please try request 'pgsql_table_list'")
        return None

    def clear_old_records_from_event_table(self, older_than_days: int = None):
        right_time = datetime.datetime.now() - datetime.timedelta(days=older_than_days)
        try:
            # version 1 doesnt works
            # deletion = delete(ModALBaseService).where(ModALBaseService.event_time < right_time)
            # with engine.connect() as conn:
            #     conn.execute(deletion)
            #     print(deletion.returning(ModALBaseService.event_descr))

            # version 2 cascade deletion works
            # Session = sessionmaker(autocommit=False, bind=engine)
            # sess = Session()
            # rows_deleted = sess.query(ModALBaseService).filter(ModALBaseService.event_time < right_time).delete()
            # sess.commit()

            # version 3 works
            Session = scoped_session(sessionmaker())
            Session.configure(bind=engine)
            session = Session()
            rows_deleted = session.query(ModALBaseService).filter(ModALBaseService.event_time < right_time).delete()
            session.commit()
            print(f"deleted {rows_deleted} rows")

        except Exception as e:
            err_str = f"{__class__.__name__} cant clear old records, error: {e}"
            print(err_str)
            self.logger.error(err_str)




if __name__ == '__main__':
    controller = ConnALEvent()
    controller.logger.debug("test debug")
    # print(controller.get_last_update_date_from_service("customers_bal_table"))

    kwargs = {
        "table_name": "unknown_table",
        "description": "test_event",
        "event_from": "tester"
    }
    req = controller.put_event_2service_table_updates(**kwargs)
    print(req)

    # print(controller.clear_old_records_from_event_table(older_than_days=7))

