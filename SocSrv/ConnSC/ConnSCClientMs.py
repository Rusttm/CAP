import time

from SocSrv.ConnSC.ConnSCClientMainClass import ConnSCClientMainClass

class ConnSCClientMS(ConnSCClientMainClass):
    """ socket client for telegram bot"""

    def __init__(self, name="ms"):
        super().__init__(name=name)


if __name__ == '__main__':
    connector = ConnSCClientMS(name="ms")
    to = "main"
    msg_text = "Hi, main! This message from MoiSklad. "
    connector.send_dict_2client(to=to, msg_text=msg_text)
    print("client successfully started")
    time.sleep(3)
    print(f"full received messages list: {connector.get_all_incoming_msgs()}")