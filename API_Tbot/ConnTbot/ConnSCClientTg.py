import time

from SocSrv.ConnSC.ConnSCClientMainClass import ConnSCClientMainClass

class ConnSCClientTg(ConnSCClientMainClass):
    """ socket client for telegram bot"""

    def __init__(self, name="telegram"):
        super().__init__(name=name)


if __name__ == '__main__':
    connector = ConnSCClientTg(name="telegram")
    to = "main"
    msg_text = "Hi, main! This message from telegrambot. "
    connector.send_dict_2client(to=to, msg_text=msg_text)
    print("client successfully started")
    time.sleep(3)
    print(f"full received messages list: {connector.get_all_incoming_msgs()}")