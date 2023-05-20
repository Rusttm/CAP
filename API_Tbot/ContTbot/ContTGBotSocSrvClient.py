import time
from API_Tbot.ConnTbot.ConnTGBotSocSrvClient import ConnTGBotSocSrvClient

class ContTGBotSocSrvClient(ConnTGBotSocSrvClient):
    """ socket client for telegram bot"""

    def __init__(self, name="telegram"):
        super().__init__(name=name)

    def send_socket_msg(self, to_user=None, msg_text=None):
        if to_user and msg_text:
            try:
                self.send_dict_2client(to_user=to_user, msg_text=msg_text)
                return True
            except Exception as e:
                self.logger.warning(f"{__name__} cant send msg to {to_user} error: {e}")
                # print(f"{__name__} cant send msg to {to_user}")
                return False
        else:
            self.logger.warning(f"{__name__} cant send msg to {to_user} empty fields 'to_user' or 'msg_text'")
            return False


if __name__ == '__main__':
    connector = ContTGBotSocSrvClient(name="telegram")
    print("client successfully started")
    name = "telegram"
    to = "admin"

    for i in range(10):
        msg_text = f"Hi, admin! This {i} message from telegrambot. "
        connector.send_socket_msg(to_user=to, msg_text=msg_text)
        time.sleep(3)
        print(f"{name} received messages list: {connector.get_all_incoming_msgs()}")
        print(f"{name} send messages list: {connector.get_all_outgoing_msgs()}")