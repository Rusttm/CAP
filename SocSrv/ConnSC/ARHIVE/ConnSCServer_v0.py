from SocSrv.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select


class ConnSCServer(SocketMainClass):
    """ starts socket server"""
    server_port = 1977
    client_tg_port = 1978
    __recv_msg_dict = dict()
    __send_msg_dict = dict()
    """ dictionary {"server": ["msg1", msg2, .. ], "client1": ["msg1", msg2]}"""

    def __init__(self):
        super().__init__()

    def start_socket_server(self):
        with socket(AF_INET, SOCK_STREAM) as server_socket:
            server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            server_socket.bind(('', self.server_port))
            server_socket.listen(1)
            server_socket.settimeout(1)
            client_sockets = []
            while True:
                try:
                    client_socket, address = server_socket.accept()
                except OSError as e:
                    # print(e)
                    pass
                else:
                    client_sockets.append(client_socket)
                finally:
                    for client_socket in client_sockets:
                        client_for_read = []
                        client_for_send = []
                        client_suspend = []
                        client_for_read, client_for_send, client_suspend = select(client_sockets,
                                                                                   client_sockets,
                                                                                   client_sockets, 0)
                        print(f"{client_for_read=}, {client_for_send=}, {client_suspend=}")
                        if client_socket in client_for_read:
                            recv_data = client_socket.recv(1024)
                            msg_list = self.__recv_msg_dict.get(address, [])
                            # print(f"message {recv_data} recieved from {address}")
                            if recv_data:
                                self.__recv_msg_dict[address] = msg_list.append(recv_data)
                                print(f"message {recv_data} recieved from {address}")
                            # else:
                            #     print("cant recieve message")

                        # if client_socket in client_for_send:
                        #     print(self.__recv_msg_dict.get(address, []))
                        #     client_socket.send(message)

                            # if self.__recv_msg_dict.get(address, []):
                            #     for msg in self.__recv_msg_dict.get(address, []):
                            #         client_socket.send(msg.encode('utf-8'))
                        # client_socket.close()


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