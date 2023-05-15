from Pgsql.ConnPgsql.ConnPsqlMainClass import ConnPsqlMainClass
import psycopg2


class ConnPsqlInit(ConnPsqlMainClass):
    """initialise connection to pgsql database
    keys from config file"""
    pgsql_conn = None
    # cursor = None

    def __init__(self):
        super().__init__()
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

    def get_pgsql_version(self):
        if self.pgsql_conn:
            try:
                with self.pgsql_conn:
                    with self.pgsql_conn.cursor() as my_cursor:
                        my_cursor.execute('SELECT version()')
                        db_version = my_cursor.fetchone()
                        my_cursor.close()
            finally:
                self.pgsql_conn.close()
        else:
            return None
        return db_version




if __name__ == '__main__':
    connector = ConnPsqlInit()
    print(connector.get_pgsql_version())
