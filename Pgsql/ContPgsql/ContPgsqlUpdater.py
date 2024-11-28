from Pgsql.ContPgsql.ContPgsqlMainClass import ContPgsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlDataGet import ConnPgsqlDataGet
from Pgsql.ConnPgsql.ConnPgsqlDataPut import ConnPgsqlDataPut
from Pgsql.ConnPgsql.ConnPgsqlDataHandler import ConnPgsqlDataHandler
from Pgsql.ConnPgsql.ConnPgsqlRowCount import ConnPgsqlRowCount
from Pgsql.ContPgsql.ContPgsqlEvent import ContPgsqlEvent
import datetime
import time
from tqdm import tqdm

class ContPgsqlUpdater(ContPgsqlMainClass, ConnPgsqlDataGet, ConnPgsqlDataPut, ConnPgsqlDataHandler, ConnPgsqlRowCount, ContPgsqlEvent):

    def __init__(self):
        super().__init__()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()


    def update_all_report_tables(self):
        """ auto updater get info from service table and update table automatically"""
        result_messages = []
        from API_MS.MSMain import MSMain
        ms_connector = MSMain()
        for table_name, data_dict in self.tables_dict.items():
            # at first get info sql_upd in tables dict
            if data_dict.get('sql_upd', None) != 1:
                continue
            # in second get function from MS controllers in MsMain
            table_data_function = data_dict.get('function', None)
            if not table_data_function:
                continue
            request_func = getattr(ms_connector, table_data_function)
            # get information about last update for table
            try:
                ans = self.get_last_update_date_from_service(evenst_table=table_name)
                from_date = str(min(ans[0][-1], ans[0][-2]))
            except:
                self.logger.error(f"{__class__.__name__} cant get last data update")
                from_date = "2024-01-01"
            to_date = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}"
            # req_data = request_func()
            req_data = request_func(from_date=from_date, to_date=to_date)
            data_list = req_data.get('data', [])
            field_table = data_dict.get('fields_table')
            fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
            gen_start = time.time()
            print(f"start :{time.ctime()} updating table: {table_name} positions: {len(data_list)}")
            time.sleep(1)
            # for i, data_string in enumerate(data_list):
            for i in tqdm(range(len(data_list))):
                data_string = data_list[i]
                col_names_list, col_values_list = self.col_and_values_list_pre_handler(table_name=table_name,
                                                                                       data_string=data_string,
                                                                                       fields_dict=fields_dict)
                self.put_data_2table(table_name=table_name, col_names_list=col_names_list,
                                     col_values_list=col_values_list)
            end = time.time()
            rows_in_table = self.count_rows_in_table(table_name=table_name)
            event_string = f"table: {table_name} ({rows_in_table}rows from {len(data_list)}) updated in {round(end - gen_start, 2)}sec\n"
            result_messages.append(event_string)
            print(event_string)
            self.put_event_2service_table_updates(table_name=table_name, description=event_string, from_date=from_date, to_date=to_date)
        return result_messages


    def get_last_update_date_from_service(self, event_table=None):
        """ return last date of update table"""

        req_line = f"SELECT event_table, event_from, MAX(event_time), MAX (event_period_end) " \
                   f"FROM pgsql_service " \
                   f"WHERE event_table='{event_table}' AND event_from='updater' " \
                   f"GROUP BY event_table, event_from"
        if event_table:
            try:
                ans = self.send_get_request(req_line=req_line)
                return ans
            except Exception as e:
                # print(e)
                self.logger.error(f"{__class__.__name__} error while request last update date {event_table}: {e}")
        else:
            self.logger.warning(f"{__class__.__name__} request not specified event_table_name={event_table}")
            self.logger.info(f"{__class__.__name__} please try request 'pgsql_table_list'")
        return None


if __name__ == '__main__':
    connector = ContPgsqlUpdater()
    print(f"tables update {connector.update_all_report_tables()}")
    # print(f"try to get table 'test' result = {connector.get_table(table_name='test')}")