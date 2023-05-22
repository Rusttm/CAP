from CAPMain.ContMain.ContCAPMainClass import ContCAPMainClass
from API_Tbot.TGBotMain import TGBotMain


# class ContCAPTGBot(ContCAPMainClass, TGBotMain):
class ContCAPTGBot(TGBotMain, ContCAPMainClass):
    """ Telegram Bot API main controller"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ContCAPTGBot started")


if __name__ == '__main__':
    connector = ContCAPTGBot()
    print("bot is working ...")
    connector.send_service_msg(msg=f"Hello, my service")
