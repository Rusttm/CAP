import time
from SocSrv.ContSC.ContSCMainClass import ContSCMainClass
from SocSrv.ConnSC.ConnSCClientAdmin import ConnSCClientAdmin


class ContSCClientAdmin(ConnSCClientAdmin, ContSCMainClass):
    client_name = "admin"
    def __init__(self):
        super().__init__()

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
    def send_socket_msg_dict(self, msg_dict: dict):
        if msg_dict:
            try:
                # self.send_dict_2client(to_user=to_user, msg_text=msg_text)
                msg_dict["from"] = self.client_name
                self.send_msg_dict_2client(msg_dict=msg_dict)
                return True
            except Exception as e:
                self.logger.warning(f"{__name__} cant send msg to {msg_dict.get('to', 'unknown')} error: {e}")
                # print(f"{__name__} cant send msg to {to_user}")
                return False
        else:
            self.logger.warning(f"{__name__} cant send msg to {msg_dict.get('to', 'unknown')} empty fields 'to_user' or 'msg_text'")
            return False
if __name__ == '__main__':
    controller = ContSCClientAdmin()
    name = "admin"
    to = "server"
    print(f"{name} client successfully started")
    for i in range(100):
        time.sleep(3)
        print(f"{name} received messages list: {controller.get_all_incoming_msgs()}")
        print(f"{name} send messages list: {controller.get_all_outgoing_msgs()}")
        msg_text = f"Hi, server! This {i} message from admin. "
        controller.send_socket_msg(to_user=to, msg_text=msg_text)