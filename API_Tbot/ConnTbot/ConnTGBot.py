from API_Tbot.TGBotMainClass import TGBotMainClass

class ConnTGBot(TGBotMainClass):
    """ Connector"""

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ConnTGBot()
    connector.logger.info("resting")