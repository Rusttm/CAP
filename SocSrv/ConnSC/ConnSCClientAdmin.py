import time

from SocSrv.ConnSC.ConnSCClientMainClass import ConnSCClientMainClass

class ConnSCClientAdmin(ConnSCClientMainClass):
    """ socket client for telegram bot"""

    def __init__(self, name="admin"):
        super().__init__(name=name)


if __name__ == '__main__':
    connector = ConnSCClientAdmin()
    name = "admin"
    to = "server"
    msg_text = "Hi, server! This message from admin. "
    connector.send_dict_2client(to_user=to, msg_text=msg_text)
    print(f"{name} client successfully started")
    time.sleep(3)
    print(f"{name} full received messages list: {connector.get_all_incoming_msgs()}")