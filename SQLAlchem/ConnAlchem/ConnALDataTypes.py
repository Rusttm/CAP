from SQLAlchem.ConnAlchem.ConnALMainClass import ConnALMainClass


class ConnALDataTypes(ConnALMainClass):
    __types_pgsql: dict[str, str] | None

    def __init__(self):
        super().__init__()
        from SQLAlchem.ConnAlchem.ConnAlJson import ConnAlJson
        self.__types_pgsql = ConnAlJson().get_data_from_json(file_name='alchemy_pgsql_mapper')


    def types_mapper(self, type_ms):
        return self.__types_pgsql.get(type_ms, f"unknown_{type_ms}")


if __name__ == '__main__':
    connector = ConnALDataTypes()
    print(connector.types_mapper("Meta"))