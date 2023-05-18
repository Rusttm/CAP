from SocSrv.ConnSC.ConnSCClientMainClass import ConnSCClientMainClass

class ConnSCClientTg(ConnSCClientMainClass):
    """ socket client for telegram bot"""

    def __init__(self):
        super().__init__(name="telegram")
        self.set_client_name("telegram")

if __name__ == '__main__':
    connector = ConnSCClientMainClass()
    to = "main"
    msg_text = "Hi, main! This message from telegrambot. "
    connector.send_dict_2client(to=to, msg_text=msg_text)
    print("client successfully started")
    print(f"full received messages list: {connector.get_all_incoming_msgs()}")