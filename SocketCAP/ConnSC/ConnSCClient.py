from SocketCAP.SocketMainClass import SocketMainClass
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

    def __init__(self):
        super().__init__()

    def send_2server(self, message=None):
        pass

    def recv_from_server(self):
        HOST = (socket.gethostname(), self.server_port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(HOST)
        print(f"connect server {HOST}")
        msg = client_socket.recv(self.buffer)
        print(msg.decode('utf-8'))


if __name__ == '__main__':
    connector = ConnSCClient()
    # print(connector.send_2server(message="Hi Server from 1978"))
    print(connector.recv_from_server())