from Pgsql.PgsqlMainClass import PgsqlMainClass
import psycopg2


class ConnPgsqlMainClass(PgsqlMainClass):
    """initialise connection to pgsql database
        keys from config file"""
    pgsql_conn = None

    def __init__(self):
        super().__init__()
        # from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
        # self.types_mapper = ConnPgsqlJson().get_data_from_json(file_name='mapper')

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

    # def send_get_request(self, req_line=None):
    #     self.init_connection()
    #     if req_line:
    #         req_line = req_line.replace("\n", "")
    #         if self.pgsql_conn:
    #             try:
    #                 with self.pgsql_conn:
    #                     # make cursor
    #                     with self.pgsql_conn.cursor() as my_cursor:
    #                         my_cursor.execute(req_line)
    #                         self.pgsql_conn.commit()
    #                         db_answer = my_cursor.fetchall()
    #                         self.logger.debug(f"{__class__.__name__} fetch cursor -'{req_line}'")
    #                         # my_cursor.close()
    #                         # self.logger.debug(f"{__class__.__name__} closed cursor -'{req_line}'")
    #                 return db_answer
    #             except Exception as e:
    #                 self.logger.error(f"{__class__.__name__} can't request: '{e}'")
    #             finally:
    #                 self.pgsql_conn.close()
    #                 self.logger.debug(f"{__class__.__name__} closed connector")
    #     else:
    #         self.logger.error(f"{__class__.__name__} command line for request is not valid-'{req_line}'")
    #     return None

    def send_get_request(self, req_line=None):
        self.init_connection()
        if req_line:
            req_line = req_line.replace("\n", "")
            if self.pgsql_conn:
                try:
                    with self.pgsql_conn as connection:
                        # make cursor
                        with connection.cursor() as my_cursor:
                            my_cursor.execute(req_line)
                            connection.commit()
                            db_answer = my_cursor.fetchall()
                            self.logger.debug(f"{__class__.__name__} fetch cursor -'{req_line}'")
                            # my_cursor.close()
                            # self.logger.debug(f"{__class__.__name__} closed cursor -'{req_line}'")
                    return db_answer
                except Exception as e:
                    self.logger.error(f"{__class__.__name__} can't request: '{e}'")
                finally:
                    self.pgsql_conn.close()
                    self.logger.debug(f"{__class__.__name__} closed connector")
        else:
            self.logger.error(f"{__class__.__name__} command line for request is not valid-'{req_line}'")
        return None


    def send_set_request(self, req_line=None):
        self.init_connection()
        if req_line:
            req_line = req_line.replace("\n", "")
            if self.pgsql_conn:
                try:
                    with self.pgsql_conn as connection:
                        # make cursor
                        with connection.cursor() as my_cursor:
                            my_cursor.execute(req_line)
                            self.logger.debug(f"{__class__.__name__} fetch cursor -'{req_line}'")
                            result_cursor = ['created!']
                            try:
                                result_cursor = my_cursor.connection.notices
                            except Exception as e:
                                print(e)
                            connection.commit()
                            self.logger.debug(f"{__class__.__name__} closed cursor -'{req_line}'")
                    return dict({"result": result_cursor})
                except Exception as e:
                    self.logger.error(f"{__class__.__name__} request error'{e}'")
                finally:
                    self.pgsql_conn.close()
                    self.logger.debug(f"{__class__.__name__} closed connector")
            else:
                self.logger.debug(f"{__class__.__name__} connector not valid == '{self.pgsql_conn}'")
        else:
            self.logger.error(f"{__class__.__name__} command line for request is not valid-'{req_line}'")
        return None

    # def types_mapper(self, type_ms):
    #     """ mapper fo datatypes from MoiSklad to Postgresql"""
    #     mapper = dict({
    #         "String(255)": "VARCHAR(255)",
    #         "Boolean": "BOOLEAN",
    #         "UUID": "UUID",
    #         "Array(Object)": "JSON[]",
    #         "Object": "JSON",
    #         "Meta": "JSON",
    #         "String(4096)": "TEXT",
    #         "Int": "INTEGER",
    #         "MetaArray": "JSON[]",
    #         "String": "TEXT",
    #         "Enum": "VARCHAR(255)", # no enum in postgresql
    #         "DateTime": "TIMESTAMP",
    #         "Float": "REAL",
    #         "Array(String)": "TEXT[]"
    #     })
    #     return mapper.get(type_ms, type_ms)


if __name__ == '__main__':
    connector = ConnPgsqlMainClass()
    ans = connector.send_get_request("SELECT version()")
    # ans = connector.send_set_request("CREATE TABLE testtable (i integer);")
    print(ans)
