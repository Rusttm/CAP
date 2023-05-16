from SocketCAP.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
import sys
import socket
import selectors
import types

class ConnSCServer(SocketMainClass):
    """ starts socket server"""
    host = 'localhost'
    server_port = 1977
    client_tg_port = 1978
    __recv_msg_dict = dict()
    __send_msg_dict = dict()
    """ dictionary {"server": ["msg1", msg2, .. ], "client1": ["msg1", msg2]}"""

    def __init__(self):
        super().__init__()

    def start_socket_server(self):
        pass

    def get_socket_msg(self):
        """ return msg dict and clear(!) it after request"""
        msg_dictionary = self.__recv_msg_dict
        self.__recv_msg_dict = dict({"server": []})
        return msg_dictionary

    def send_socket_msg(self, socket_name=None, msg=None):
        if socket_name and msg:
            self.__send_msg_dict[socket_name] = self.__send_msg_dict.get(socket_name, []).append(msg)


if __name__ == '__main__':
    connector = ConnSCServer()
    print(connector.start_socket_server())