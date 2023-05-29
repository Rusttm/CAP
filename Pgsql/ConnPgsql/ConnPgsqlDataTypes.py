from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass


class ConnPgsqlDataTypes(ConnPgsqlMainClass):

    __types_pgsql: dict[str, str] | None

    def __init__(self):
        super().__init__()
        from Pgsql.ConnPgsql.ConnPgsqlJson import ConnPgsqlJson
        self.__types_pgsql = ConnPgsqlJson().get_data_from_json(file_name='mapper')


    def types_mapper(self, type_ms):
        return self.__types_pgsql.get(type_ms, type_ms)


if __name__ == '__main__':
    connector = ConnPgsqlDataTypes()
    print(connector.types_mapper("Meta"))