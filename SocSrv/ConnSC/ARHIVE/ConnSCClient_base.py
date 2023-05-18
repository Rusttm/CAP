import pickle

from SocSrv.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM
import sys
import socket
import selectors
import types

class ConnSCClient(SocketMainClass):
    """ client for reader client"""
    server_port = 1977
    server_host = 'localhost'
    buffer = 1024 #bytes
    conn_num = 5
    client_socket = None
    HOST = None

    def __init__(self):
        super().__init__()
        self.HOST = (socket.gethostname(), self.server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg_2server(self, message=None):
        self.client_socket.connect(self.HOST)
        self.logger.debug(f"{__class__.__name__} client connect to server {self.HOST} for send message")
        msg_head = f"GET / HTTP/1.1\r\nHost:localhost:{self.server_port}\r\n\r\n"
        msg = msg_head + message
        self.client_socket.sendall(msg.encode('utf-8'))
        self.logger.debug(f"{__class__.__name__} client send msg to server {self.HOST}")

    def send_dict_2server(self, dictionary=None):
        self.client_socket.connect(self.HOST)
        self.logger.debug(f"{__class__.__name__} client connect to server {self.HOST} for send dict")
        if not dictionary:
            dictionary = dict({"error": "no data to send"})
        msg = pickle.dumps(dictionary)
        self.client_socket.sendall(msg)
        self.logger.debug(f"{__class__.__name__} client send dict to server {self.HOST}")

    def recv_msg_from_server(self):
        self.client_socket.connect(self.HOST)
        self.logger.debug(f"{__class__.__name__} client connect to server {self.HOST} to receive message")
        msg = ""
        while True:
            data = self.client_socket.recv(self.buffer)
            # try to wide limits
            if not len(data) or len(msg) > self.buffer * 2:
                break
            msg += data.decode('utf-8')
            print(f"received {msg}")

    def recv_dict_from_server(self):
        self.client_socket.connect(self.HOST)
        self.logger.debug(f"{__class__.__name__} client connect server {self.HOST} for receive dictionary")
        data = self.client_socket.recv(self.buffer)
        msg = pickle.loads(data)
        print(f"received {msg}")
        return True


if __name__ == '__main__':
    connector = ConnSCClient()
    my_dictionary = dict({"module": "telegram", "data": {"from": "57685837", "text": "hello telegram"}})
    # print(connector.send_2server(message=f"Hi Server from client {connector.HOST}"))
    # print(connector.recv_dict_from_server())
    print(connector.send_dict_2server(dictionary=my_dictionary))