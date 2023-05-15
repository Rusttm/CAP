from Main.CAPMainClass import CAPMainClass
import psycopg2


class ConnPsqlMainClass(CAPMainClass):
    """initialise connection to pgsql database
        keys from config file"""
    pgsql_conn = None

    def __init__(self):
        super().__init__()

    def init_connection(self):
        from Pgsql.ConnPgsql.ConnPgsqlConfig import ConnPgsqlConfig
        try:
            conf = ConnPgsqlConfig().get_config()
            self.pgsql_conn = psycopg2.connect(
                host=conf['url'],
                port=conf['port'],
                database=conf['db_name'],
                user=conf['user'],
                password=conf['user_pass'])
            # self.cursor = self.pgsql_conn.cursor()
            self.logger.debug(f"{__class__.__name__} connector for PostgreSQL created")
        except Exception as e:
            # print(f"configuration data not loaded {e}")
            self.logger.error(f"{__class__.__name__} can't create connector for PostgreSQL! {e}")

    def send_get_request(self, req_line=None):
        db_answer = None
        self.init_connection()
        if req_line:
            req_line = req_line.replace("\n", "")
            if self.pgsql_conn:
                try:
                    with self.pgsql_conn:
                        # make cursor
                        with self.pgsql_conn.cursor() as my_cursor:
                            my_cursor.execute(req_line)
                            self.pgsql_conn.commit()
                            db_answer = my_cursor.fetchall()
                            self.logger.debug(f"{__class__.__name__} fetch cursor -'{req_line}'")
                            my_cursor.close()
                            self.logger.debug(f"{__class__.__name__} closed cursor -'{req_line}'")
                finally:
                    self.pgsql_conn.close()
                    self.logger.debug(f"{__class__.__name__} closed connector")
            else:
                return None
        else:
            self.logger.error(f"{__class__.__name__} command line for request is not valid-'{req_line}'")
        return db_answer

    def send_set_request(self, req_line=None):
        self.init_connection()
        if req_line:
            req_line = req_line.replace("\n", "")
            if self.pgsql_conn:
                try:
                    with self.pgsql_conn:
                        # make cursor
                        with self.pgsql_conn.cursor() as my_cursor:
                            my_cursor.execute(req_line)
                            self.pgsql_conn.commit()
                            self.logger.debug(f"{__class__.__name__} fetch cursor -'{req_line}'")
                            my_cursor.close()
                            self.logger.debug(f"{__class__.__name__} closed cursor -'{req_line}'")
                except Exception as e:
                    self.logger.error(f"{__class__.__name__} request error'{e}'")
                finally:
                    self.pgsql_conn.close()
                    self.logger.debug(f"{__class__.__name__} closed connector")
            else:
                self.logger.debug(f"{__class__.__name__} connector not valid == '{self.pgsql_conn}'")
                return None
        else:
            self.logger.error(f"{__class__.__name__} command line for request is not valid-'{req_line}'")

if __name__ == '__main__':
    connector = ConnPsqlMainClass()
    ans = connector.send_get_request("SELECT version()")
    ans = connector.send_set_request("CREATE TABLE testtable (i integer);")
    print(ans)