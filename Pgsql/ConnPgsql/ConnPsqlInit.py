from Pgsql.ConnPgsql.ConnPsqlMainClass import ConnPsqlMainClass
import psycopg2

class ConnPsqlInit(ConnPsqlMainClass):
    pgsql_conn = None
    def __init__(self):
        super().__init__()
        # self.pgsql_conn = psycopg2.connect("dbname=capdb user=capuser password=cap_pass")
        self.pgsql_conn = psycopg2.connect(
            host="192.168.1.80:5432",
            database="capdb",
            user="capuser",
            password="cap_pass")
        self.cursor = self.pgsql_conn.cursor()

    def get_pgsql_version(self):
        self.cursor.execute('SELECT version()')
        db_version = self.cursor.fetchone()
        print(db_version)
        self.cursor.close()

if __name__ == '__main__':
    connector = ConnPsqlInit()
    connector.get_pgsql_version()