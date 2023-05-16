from SocketCAP.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM


class ConnSCClient(SocketMainClass):
    """ client for reader client"""
    client_port = 1977

    def __init__(self):
        super().__init__()

    def send_2server(self, message=None):
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', self.client_port))
            client_socket.send(message.encode('utf-8'))
            # while True:
            #     client_socket.send(message.encode('utf-8'))

    def recv_from_server(self):
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect(('localhost', self.client_port))
            while True:
                data = client_socket.recv(1024)
                print(f"response from server: {data.decode('utf-8')} length {len(data)}")


if __name__ == '__main__':
    connector = ConnSCClient()
    print(connector.send_2server(message="Hi Server from 1978"))