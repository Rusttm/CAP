from PgsqlAlchemy.ModALFillers.ModALFillerMainClass import ModALFillerMainClass
import datetime
from PgsqlAlchemy.ModALFillers.ModALFillerMainClass import ModALFillerMainClass
from PgsqlAlchemy.ModAL.ModALBaseCustBal import ModALBaseCustBal
from PgsqlAlchemy.ConnAL.ConnALMainClass import ConnALMainClass
from PgsqlAlchemy.ContMS.ContMSMain import ContMSMain

from sqlalchemy import create_engine, select, text, func
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import pandas as pd

__url = ConnALMainClass().get_url()
engine = create_engine(__url)


class ModALFillEvent(ModALFillerMainClass):

    def __init__(self):
        super().__init__()

    def put_event_2service_table_updates(self, table_name=None,
                                         description=None,
                                         from_date=None,
                                         to_date=None):
        """ put in service table information about updates of tables"""
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d %H:%M:%S")
        if not from_date:
            from_date = "2023-05-01 00:00:00"
        if not to_date:
            to_date = date_string
        event_dict = {"event_name": "table_updated",
                      "event_descr": f"new updates in table {table_name}: {description}",
                      "event_to": "telegram",
                      "event_from": "updater",
                      "event_level": 10,
                      "event_active": False,
                      "event_table": table_name,
                      "event_time": date_string,
                      "event_period_start": from_date,
                      "event_period_end": to_date}
        # self.put_event(event_dict)

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


if __name__ == '__main__':
    controller = ModALFillEvent()
    print(controller.get_last_update_date_from_service("customers_bal_table"))
    # controller.put_event_2service_table_updates(table_name='unknown_table')
