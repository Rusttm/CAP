from SocSrv.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
import sys
import socket
import selectors
import types
import pickle

class ConnSCServer(SocketMainClass):
    """ starts socket server"""
    host = 'localhost'
    server_port = 1977
    client_tg_port = 1978
    server_socket = None
    buffer = 1024
    __recv_msg_dict = dict()
    __send_msg_dict = dict()
    """ dictionary {"server": ["msg1", msg2, .. ], "client1": ["msg1", msg2]}"""

    def __init__(self):
        super().__init__()
        self.start_socket_server()


    def start_socket_server(self):
        # print(socket.gethostname())
        HOST = (socket.gethostname(), self.server_port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse address in OS after closing (notimeout)
        self.server_socket.bind(HOST)
        self.server_socket.listen()
        self.logger.debug(f"{__class__.__name__} server initiated and listening port {self.server_port}")

    def get_client_msg(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.logger.debug(f"{__class__.__name__} server connected to client {addr} for receiving msg")
            msg = ""
            while True:
                data = client_socket.recv(self.buffer)
                # if msg is mach longer
                if not len(data) or len(msg) > self.buffer * 2:
                    break
                msg += data.decode('utf-8')
            print(f"received {msg}")
            self.logger.debug(f"{__class__.__name__} server receive msg {msg} from client {addr}")
            client_socket.close()  # should close connection
            self.logger.debug(f"{__class__.__name__} server close connection to client {addr}")

    def get_client_dict(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.logger.debug(f"{__class__.__name__} server connected to client {addr} for receiving dict")
            data = client_socket.recv(self.buffer)
            msg = pickle.loads(data)
            print(f"received {msg}")
            self.logger.debug(f"{__class__.__name__} server receive dict {msg} from client {addr}")
            client_socket.close()  # should close connection
            self.logger.debug(f"{__class__.__name__} server close connection to client {addr}")

    def send_2client_msg(self, msg=None):
        while True:
            self.logger.debug(f"{__class__.__name__} server connecting to client {addr} for send msg")
            client_socket, addr = self.server_socket.accept()
            self.logger.debug(f"{__class__.__name__} server connected to client {addr} for send msg")
            if not msg:
                msg = f'Hello to {addr} from server'
            client_socket.sendall(msg.encode('utf-8'))
            self.logger.debug(f"{__class__.__name__} server send msg client {addr}")
            client_socket.close()  # should close connection
            self.logger.debug(f"{__class__.__name__} server close connection to client {addr}")

    def send_2client_dict(self, dictionary=None):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.logger.debug(f"{__class__.__name__} server connected to client {addr} for send dictionary")
            if not dictionary:
                dictionary = dict({"error": "no data to send"})
            msg = pickle.dumps(dictionary)
            client_socket.sendall(msg)
            self.logger.debug(f"{__class__.__name__} server send dictionary to client {addr}")
            client_socket.close()  # should close connection


if __name__ == '__main__':
    connector = ConnSCServer()
    my_dictionary = dict({"module": "telegram", "data": {"from": "57685837", "text": "hello telegram"}})
    # print(connector.send_2client_dict(my_dictionary))
    print(connector.get_client_dict())