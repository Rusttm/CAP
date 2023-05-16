from SocketCAP.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
import sys
import socket
import selectors
import types
import pickle
import select


class ConnSCServer(SocketMainClass):
    """ starts socket server"""
    host = 'localhost'
    server_port = 1977
    client_tg_port = 1978
    server_socket = None
    buffer = 1024
    sockets_list = []
    clients_dict = {}
    header_length = 10
    __recv_msg_dict = dict()
    __send_msg_dict = dict()
    """ dictionary {"server": ["msg1", msg2, .. ], "client1": ["msg1", msg2]}"""

    def __init__(self):
        super().__init__()
        self.start_socket_server()

    def start_socket_server(self):
        # print(socket.gethostname())
        self.host = (socket.gethostname(), self.server_port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                      1)  # reuse address in OS after closing (notimeout)
        self.server_socket.bind(self.host)
        self.server_socket.listen()
        self.sockets_list.append(self.server_socket)
        self.logger.debug(f"{__class__.__name__} server initiated and listening port {self.server_port}")
# main version
    # def get_client_msg(self, client_socket: socket.socket):
    #     # recieve header with len of msg and usei it like buffer
    #     try:
    #         msg_header = client_socket.recv(self.header_length)
    #         if not len(msg_header):
    #             self.logger.error(f"{__class__.__name__} server error: header_length is null")
    #             return False
    #         msg_length = int(msg_header.decode('utf-8').strip())
    #         return {'header': msg_header, 'data': client_socket.recv(msg_length).decode('utf-8')}
    #     except Exception as e:
    #         self.logger.error(f"{__class__.__name__} server error: {e}")
    #         return False

# this version without headers
    def get_client_msg(self, client_socket: socket.socket):
        # recieve header with len of msg and usei it like buffer
        try:
            msg = client_socket.recv(self.buffer)
            # if not len(msg_header):
            #     self.logger.error(f"{__class__.__name__} server error: header_length is null")
            #     return False
            # msg_length = int(msg_header.decode('utf-8').strip())
            print(f"message {msg.decode('utf-8')} received!!!")
            return msg.decode('utf-8')
        except Exception as e:
            self.logger.error(f"{__class__.__name__} server error: {e}")
            return False

    def listen_2receive_msg(self):
        client_sockets = self.sockets_list
        while 1:
            client_for_read, client_for_send, client_exceptional = select.select(client_sockets,
                                                                                 client_sockets,
                                                                                 client_sockets, 1)
            for _socket in client_for_read:
                if _socket == self.server_socket:
                    """ if server ready to read """
                    client_socket, addr = self.server_socket.accept()
                    user = self.get_client_msg(client_socket=client_socket)
                    if not user:
                        continue
                    self.sockets_list.append(client_socket)
                    self.clients_dict[client_socket] = user
                else:
                    client_socket, addr = self.server_socket.accept()
                    msg = self.get_client_msg(client_socket=client_socket)
                    if not msg:
                        """ if msg empty delete clients from sockets_list and clients_dict"""
                        self.logger.debug(f"{__class__.__name__} server interrupt client {addr} msg is null")
                        self.sockets_list.remove(_socket) # remove from list
                        del self.clients_dict[_socket] # remove from dict
                        continue
                    user = self.clients_dict[_socket]

                    for client_socket in self.clients_dict.keys():
                        if client_socket is not _socket:
                            """ spam for other users"""
                            client_socket.sendall(f" new message from {user['data']} is {msg['data']}")

                for _socket in client_exceptional:
                    """ remove sockets with errors from sockets_list and clients_dict """
                    self.sockets_list.remove(_socket)
                    del self.clients_dict[_socket]

    # def get_client_dict(self):
    #     while True:
    #         client_socket, addr = self.server_socket.accept()
    #         self.logger.debug(f"{__class__.__name__} server connected to client {addr} for receiving dict")
    #         data = client_socket.recv(self.buffer)
    #         msg = pickle.loads(data)
    #         print(f"received {msg}")
    #         self.logger.debug(f"{__class__.__name__} server receive dict {msg} from client {addr}")
    #         client_socket.close()  # should close connection
    #         self.logger.debug(f"{__class__.__name__} server close connection to client {addr}")
    #
    # def send_2client_msg(self, msg=None):
    #     while True:
    #         self.logger.debug(f"{__class__.__name__} server connecting to client {addr} for send msg")
    #         client_socket, addr = self.server_socket.accept()
    #         self.logger.debug(f"{__class__.__name__} server connected to client {addr} for send msg")
    #         if not msg:
    #             msg = f'Hello to {addr} from server'
    #         client_socket.sendall(msg.encode('utf-8'))
    #         self.logger.debug(f"{__class__.__name__} server send msg client {addr}")
    #         client_socket.close()  # should close connection
    #         self.logger.debug(f"{__class__.__name__} server close connection to client {addr}")
    #
    # def send_2client_dict(self, dictionary=None):
    #     while True:
    #         client_socket, addr = self.server_socket.accept()
    #         self.logger.debug(f"{__class__.__name__} server connected to client {addr} for send dictionary")
    #         if not dictionary:
    #             dictionary = dict({"error": "no data to send"})
    #         msg = pickle.dumps(dictionary)
    #         client_socket.sendall(msg)
    #         self.logger.debug(f"{__class__.__name__} server send dictionary to client {addr}")
    #         client_socket.close()  # should close connection


if __name__ == '__main__':
    connector = ConnSCServer()
    # my_dictionary = dict({"module": "telegram", "data": {"from": "57685837", "text": "hello telegram"}})
    # print(connector.send_2client_dict(my_dictionary))
    print(connector.listen_2receive_msg())
