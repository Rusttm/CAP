from Pgsql.ConnPgsql.ConnPgsqlMainClass import ConnPgsqlMainClass



class ConnPgsqlDataHandler(ConnPgsqlMainClass):
    def __init__(self):
        super().__init__()
        from Pgsql.ContPgsql.ContPgsqlReadJsonTablesDict import ContPgsqlReadJsonTablesDict
        self.tables_dict = ContPgsqlReadJsonTablesDict().get_tables_dict()

    def col_and_values_list_pre_handler(self, data_string, table_name, fields_dict=None):
        """ add '' for json and cast array[]::json[] and array[]::text[] to list
        return corrected """
        # from Pgsql.ConnPgsql.ConnPgsqlDataTypes import ConnPgsqlDataTypes
        col_names_list = []
        col_values_list = []
        if fields_dict is None:
            field_table = self.tables_dict.get(table_name)['fields_table']
            fields_dict = self.get_pgtype_info_fields_table(field_table_name=field_table)
        for col_name, col_value in dict(data_string).items():
            if col_name == "group":
                col_name = "group_ms"
            if col_value is None:
                continue
            # field_table = dict(self.tables_dict).get(table_name)['fields_table']
            col_type = fields_dict.get(col_name, None)
            # sometimes in data presence new columns
            if col_type is None:
                warn_string = f"column {col_name} doesnt have datatype in {table_name}"
                warn_string += f"please declare {col_name} in configuration file!"
                print(warn_string)
                self.logger.warning(warn_string)
                continue
            col_names_list.append(col_name)
            if type(col_value) == str:
                col_value = f'{col_value}'
            elif col_type == "JSON":
                # "name": "ООО "АМЕТИСТ""
                for key, value in col_value.items():
                    if type(value) == str:
                        value = value.replace('"', "")
                    col_value[key] = value
                col_value = str(col_value).replace("'", '"')
                # col_value = f"'{col_value}'"
            elif col_type == "TEXT[]":
                new_string_array = []
                if type(col_value) == list:
                    for string_elem in col_value:
                        # string_elem = str(string_elem).replace('"', "")
                        new_string_array.append(string_elem)
                col_value = 'array' + f'{new_string_array}' + '::text[]'
            elif col_type == "JSON[]":
                """ returns "array['{"meta": {"href": "https://api.moysklad.ru/api/remap/1.2/entity/product/068dc1cd-cf1a-11ee-0a80-132f003e93fe/files", "type": "files", "mediaType": "application/json", "size": 0, "limit": 1000, "offset": 0}}']::json[]" """
                new_json_array = []
                # single json[] not like list, but like json
                if type(col_value) == list:
                    for json_elem in col_value:
                        json_elem = str(json_elem).replace("'", '"')
                        new_json_array.append(json_elem)
                else:
                    json_elem = str(col_value).replace("'", '"')
                    new_json_array.append(json_elem)
                col_value = 'array' + f'{new_json_array}' + '::json[]'
            col_values_list.append(col_value)
        return col_names_list, col_values_list

    def get_pgtype_info_fields_table_bckp(self, field_table_name=None):
        from Pgsql.ConnPgsql.ConnPgsqlData import ConnPgsqlData
        connector = ConnPgsqlData()
        table_data = connector.get_cols_from_table(table_name=field_table_name, col_list=['field_name', 'field_pg_type'])
        return dict(table_data)

    def  get_pgtype_info_fields_table(self, field_table_name=None):
        temp_dict = {'accountId': 'UUID', 'alcoholic': 'Object', 'archived': 'Boolean', 'article': 'String(255)',
                     'attributes': 'Array(Object)', 'barcodes': 'Array(Object)', 'buyPrice': 'Object',
                     'code': 'String(255)', 'country': 'Meta', 'description': 'String(4096)',
                     'discountProhibited': 'Boolean', 'effectiveVat': 'Int', 'effectiveVatEnabled': 'Boolean',
                     'externalCode': 'String(255)', 'files': 'JSON[]', 'group': 'Meta', 'id': 'UUID',
                     'images': 'MetaArray', 'isSerialTrackable': 'Boolean', 'meta': 'Meta', 'minPrice': 'Object',
                     'minimumBalance': 'Int', 'name': 'String(255)', 'owner': 'Meta', 'packs': 'Array(Object)',
                     'partialDisposal': 'Boolean', 'pathName': 'String', 'paymentItemType': 'Enum', 'ppeType': 'Enum',
                     'productFolder': 'Meta', 'salePrices': 'Array(Object)', 'shared': 'Boolean', 'supplier': 'Meta',
                     'syncId': 'UUID', 'taxSystem': 'Enum', 'things': 'Array(String)', 'tnved': 'String(255)',
                     'trackingType': 'Enum', 'uom': 'Meta', 'updated': 'DateTime', 'useParentVat': 'Boolean',
                     'variantsCount': 'Int', 'vat': 'Int', 'vatEnabled': 'Boolean', 'volume': 'Int', 'weight': 'Int'}
        return temp_dict