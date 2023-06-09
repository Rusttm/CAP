from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSBalance(ConnMSMainClass):
    """ connector to MoiSklad balance """
    request_url = 'url_money'
    """ requested api url"""
    request_token = 'access_token'
    """ API token"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")
        super().set_config(url_conf_key=self.request_url, token_conf_key=self.request_token)

    def get_accounts_bal(self):
        """ return dict with acconts and balance
        Example {'ПАО РОСБАНК (40702840997960000004)': 0.0, ..}"""
        json_data = self.get_api_data()
        accounts_dict = dict()
        # try to get entity accounts dict
        entity = json_data['rows'][0]['organization']['meta']['href']
        entity_accounts_href = entity + "/accounts/"
        self.set_api_url(entity_accounts_href)
        entity_accounts = None
        try:
            entity_accounts = self.get_api_data()
        except Exception as e:
            self.logger.error(f"cant request entity accounts {e}")

        for i, acc in enumerate(json_data['rows']):
            # checking rows and matching with data from entity
            if i != 0:
                try:
                    account_name = acc['account']['name']
                    if entity_accounts:
                        # looking account number in accounts dict and change values
                        for account in entity_accounts['rows']:
                            if account_name == account['accountNumber']:
                                account_name = f"{account['bankName']} ({account_name})"
                    accounts_dict[account_name] = acc['balance'] / 100
                except Exception as e:
                    # print(e)
                    self.logger.error(f"matching accounts error {e}")
        return dict(sorted(accounts_dict.items()))

    def get_sum(self):
        self.logger.debug("balance sum requested")
        data_dict = self.get_api_data()
        accounts_list = [0]
        for acc in data_dict['rows']:
            accounts_list.append(acc['balance'] / 100)
        return sum(accounts_list)


if __name__ == '__main__':
    connector = ConnMSBalance()
    print(connector.get_sum())