from API_Tbot.ContTbot.ContTGBot import ContTGBot

class TGBotMain(ContTGBot):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = TGBotMain()
    print("bot is working ...")
    connector.send_spam_msg(msg=f"Hello, everybody, iam spam")