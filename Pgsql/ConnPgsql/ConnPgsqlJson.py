from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlJson(ConnPgsqlMainClass):
    """ convert fields from json file to dict"""

    def __init__(self):
        super().__init__()

    def get_fields_from_json(self, file_name=None):
        return False


if __name__ == '__main__':
    connector = ConnPgsqlJson()
    ans = connector.get_fields_from_json("SELECT version()")
    # ans = connector.send_set_request("CREATE TABLE testtable (i integer);")
    print(ans)