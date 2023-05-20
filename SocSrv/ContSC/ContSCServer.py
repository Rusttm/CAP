import time

from SocSrv.ConnSC.ConnSCServer import ConnSCServer


class ContSCServer(ConnSCServer):

    def __init__(self):
        super().__init__()


    def get_socserver_incomings(self):
        incomed_msg_list = self.incoming_msg_list
        self.incoming_msg_list = []
        return incomed_msg_list
    def get_socserver_outgoins(self):
        outgoing_msg_list = self.outgoing_msg_list
        self.outgoing_msg_list = []
        return outgoing_msg_list


    # def socket_send_msg_2tg(self, from_user=None, msg_text=None):
    #     if msg_text and from_user:
    #         self.outgoing_msg_queue.append(dict({"from": from_user, "to": "telegram", "text": msg_text}))
    #

if __name__ == '__main__':
    controller = ContSCServer()
    print("Server runs!")
    for i in range(10):
        time.sleep(5)
        print(f"incoming messages on server {controller.get_socserver_incomings()}")
        print(f"outgoing messages on server {controller.get_socserver_outgoins()}")

    # connector.socket_send_msg_2tg(from_user="rustam", msg_text=None)
