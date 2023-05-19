from API_Tbot.ContTbot.ContMainClass import ContMainClass
from API_Tbot.ConnTbot.ConnTGBot import ConnTGBot

class ContTGBot(ContMainClass, ConnTGBot):
    """ Controller """

    def __init__(self):
        super().__init__()

    def send_service_msg(self, msg=None):
        for admin in self.users_ids['admin']:
            self.bot.send_message(chat_id=admin, text="Hello my friend", parse_mode="HTML")

    def send_finance_msg(self, msg=None):
        for fin in self.users_ids.get('fin', []):
            self.bot.send_message(chat_id=fin, text=msg, parse_mode="HTML")



if __name__ == '__main__':
    connector = ContTGBot()
    print("bot is working ...")
    connector.send_finance_msg(msg=f"Hello my finance")
    # for i in range(4):
    #     connector.send_finance_msg(msg=f"{i}Hello my friend")
    #     time.sleep(3)
