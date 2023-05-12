from Pgsql.ConnPgsql.ConnPsqlMainClass import ConnPsqlMainClass
from Pgsql.ConnPgsql.ConnPgsqlConfig import ConnPgsqlConfig
import psycopg2


class ConnPsqlInit(ConnPsqlMainClass, ConnPgsqlConfig):
    pgsql_conn = None

    def __init__(self):
        super().__init__()
        # self.pgsql_conn = psycopg2.connect("dbname=capdb user=capuser password=cap_pass")
        try:
            conf = ConnPgsqlConfig().get_config()
            self.pgsql_conn = psycopg2.connect(
                host=conf['url'],
                port=conf['port'],
                database=conf['db_name'],
                user=conf['user'],
                password=conf['user_pass'])
            self.cursor = self.pgsql_conn.cursor()
        except Exception as e:
            print(f"configuration data not loaded {e}")

    def get_pgsql_version(self):
        self.cursor.execute('SELECT version()')
        db_version = self.cursor.fetchone()
        print(db_version)
        self.cursor.close()


if __name__ == '__main__':
    connector = ConnPsqlInit()
    connector.get_pgsql_version()
