import pickle

from SocketCAP.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM
import socket
from datetime import datetime
import time



class ConnSCClientTg(SocketMainClass):
    """ client for telegram module"""
    server_port = 1977
    """ server port"""
    server_host = 'localhost'
    """ server host"""
    buffer = 1024 #bytes
    """ length of received data"""
    conn_num = 5

    client_name = "telegram"
    """ name of socket client"""
    server_msgs_list = []
    """ list of messages received from server"""

    def __init__(self):
        super().__init__()
        self.server_host = socket.gethostname()
        self.HOST = (self.server_host, self.server_port)
        """ tuple (server host, server port)"""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setblocking(0)
        self.client_socket.connect(self.HOST)
        # set buffer to not blocking during the sending information
        self.logger.debug(f"{__class__.__name__} client connect to server {self.HOST} for send dict")
        self.send_dict_2server(to="server", data=f"Telegram client starts at {datetime.now()}")

    def send_dict_2server(self, to=None, data=None):
        if not data:
            msg_dict = dict({"error": "no  recipient or data to send"})
            self.logger.debug(f"{__class__.__name__} client send to server {self.HOST} empty msg")
        if not to:
            self.logger.debug(f"{__class__.__name__} client not specified recipient, so msg send to server {self.HOST}")
            to = "server"
        msg_dict = {"from": self.client_name, "to": to, "data": data}
        msg = pickle.dumps(msg_dict)
        self.client_socket.sendall(msg)
        self.logger.debug(f"{__class__.__name__} client send dict to server {self.HOST}")

    def recv_dict_from_server(self):
        self.client_socket.connect(self.HOST)
        self.logger.debug(f"{__class__.__name__} client connect server {self.HOST} for receive dictionary")
        data = self.client_socket.recv(self.buffer)
        msg = pickle.loads(data)
        print(f"received {msg}")
        return True


if __name__ == '__main__':
    connector = ConnSCClientTg()
    for i in range(10):
        connector.send_dict_2server(to="main", data=f"Hi, Server {i}")
        print(f"send {i} packet")
        time.sleep(3)
    print("sends closed")