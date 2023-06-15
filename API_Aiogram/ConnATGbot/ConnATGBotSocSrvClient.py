import time

from API_Aiogram.ConnATGbot.ConnATGBotSocSrvMainClass import ConnATGBotSocSrvMainClass

class ConnATGBotSocSrvClient(ConnATGBotSocSrvMainClass):
    """ socket client for telegram bot"""

    def __init__(self, name="telegram"):
        super().__init__(name=name)


if __name__ == '__main__':
    connector = ConnATGBotSocSrvClient(name="telegram")
    to = "main"
    msg_text = "Hi, main! This message from telegrambot. "
    connector.send_dict_2client(to_user=to, msg_text=msg_text)
    print("client successfully started")
    time.sleep(3)
    print(f"full received messages list: {connector.get_all_incoming_msgs()}")