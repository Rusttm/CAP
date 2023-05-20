import time

from SocSrv.ConnSC.ConnSCClientTg import ConnSCClientTg


class ContSCClientTg(ConnSCClientTg):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    controller = ContSCClientTg()
    name = "telegram"
    to = "server"
    msg_text = f"Hi, server! This message from {name}. "
    controller.send_dict_2client(to=to, msg_text=msg_text)
    print(f"{name} client successfully started")
    time.sleep(3)
    print(f"{name} received messages list: {controller.get_all_incoming_msgs()}")
    print(f"{name} send messages list: {controller.get_all_outgoing_msgs()}")