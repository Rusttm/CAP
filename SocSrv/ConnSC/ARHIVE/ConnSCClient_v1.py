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
    conn_num = 5

    def __init__(self):
        super().__init__()

    def send_2server(self, message=None):
        sel = selectors.DefaultSelector()
        messages = [b"Message 1 from client.", b"Message 2 from client."]
        server_addr = (self.server_host, self.server_port)
        for i in range(0, self.conn_num):
            connid = i + 1
            print(f"Starting connection {connid} to {server_addr}")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setblocking(False)
            sock.connect_ex(server_addr)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            data = types.SimpleNamespace(
                connid=connid,
                msg_total=sum(len(m) for m in messages),
                recv_total=0,
                messages=messages.copy(),
                outb=b"",
            )
            sel.register(sock, events, data=data)

    def recv_from_server(self):
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', self.server_port))
            while True:
                data = client_socket.recv(1024)
                print(f"response from server: {data.decode('utf-8')} length {len(data)}")


if __name__ == '__main__':
    connector = ConnSCClient()
    print(connector.send_2server(message="Hi Server from 1978"))