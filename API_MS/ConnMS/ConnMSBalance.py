from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSBalance(ConnMSMainClass):
    """ connector to MoiSklad balance """

    def __init__(self):
        super().__init__()

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
            self.logger.error("cant request entity accounts")
            print(e)

        for i, acc in enumerate(json_data['rows']):
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
                    print(e)
        self.logger.info("Accounts balance successfully downloaded")
        return dict(sorted(accounts_dict.items()))

    def get_sum(self):
        json_data = self.get_api_data()
        accounts_list = [0]
        for acc in json_data['rows']:
            accounts_list.append(acc['balance'] / 100)
        self.logger.info("balance sum successfully downloaded")
        return sum(accounts_list)


if __name__ == '__main__':
    connector = ConnMSBalance()
