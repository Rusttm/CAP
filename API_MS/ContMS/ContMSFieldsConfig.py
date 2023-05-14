from API_MS.ContMS.ContMSMainClass import ContMSMainClass

class ContMSFieldsConfig(ContMSMainClass):
    """ controller for fields data
    reads excell data tables or json config files
    """

    def __init__(self):
        super().__init__()

    def read_product_fields_from_excell(self, to_file=False, excell_file_name=None, json_file_name=None):
        """ return dict data from excell file
        and save to json config file if to_file==True"""
        from API_MS.ConnMS.ConnMSReadExcell import ConnMSReadExcell
        from API_MS.ConnMS.ConnMSSaveFile import ConnMSSaveFile
        prod_fields_conf = ConnMSReadExcell().get_excell_data(file_name=excell_file_name)
        if to_file and excell_file_name:

            if not json_file_name:
                """ if json_file_name was not declare"""
                json_file_name = excell_file_name
            ConnMSSaveFile().save_data_json_file(data_dict=prod_fields_conf, file_name=json_file_name,
                                                 dir_name='config')
        return prod_fields_conf

    def read_product_fields(self, file_name=None):
        from API_MS.ConnMS.ConnMSReadJson import ConnMSReadJson
        return ConnMSReadJson().get_config_json_data(file_name=file_name)


if __name__ == '__main__':
    connector = ContMSFieldsConfig()
    # read and convert products fields config
    print(connector.read_product_fields_from_excell(to_file=True,
                                                    excell_file_name='prod_fields.xlsx',
                                                    json_file_name='product_fields.json'))
    print(connector.read_product_fields(file_name='product_fields.json'))
    print(connector.read_product_fields())
