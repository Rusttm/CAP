from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData


class ConnPgsqlEvent(ConnPgsqlMainClass):
    """ connector for service table"""
    service_table_name = 'pgsql_service'

    def __init__(self):
        super().__init__()

    def put_event(self, event_dict: dict):
        """ event should be dictionary like {'event_name':'string', 'event_descr':'', 'event_to':''} """
        # if type(event_dict) == dict:
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        col_names_list = list(event_dict.keys())
        col_values_list = list(event_dict.values())
        connector = ConnPgsqlData().put_data_2table(table_name=self.service_table_name,
                                                    col_names_list=col_names_list,
                                                    col_values_list=col_values_list)
        return True


if __name__ == '__main__':
    connector = ConnPgsqlEvent()
