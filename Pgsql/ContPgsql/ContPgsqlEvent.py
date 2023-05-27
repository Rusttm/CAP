from Pgsql.ConnPgsql.ConnPgsqlEvent import ConnPgsqlEvent
import datetime
class ContPgsqlEvent(ConnPgsqlEvent):

    def __init__(self):
        super().__init__()

    def put_event_2service_table_updates(self, table_name=None,
                                               description=None,
                                               from_date=None,
                                               to_date=None
                                               ):
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
        self.put_event(event_dict)


if __name__ == '__main__':
    controller = ContPgsqlEvent()
    controller.put_event_2service_table_updates(table_name='unknown_table')
