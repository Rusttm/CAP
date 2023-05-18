from SocSrv.SocketMainClass import SocketMainClass
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
        sel = selectors.DefaultSelector()
        # print(sys.argv)
        # self.host, self.server_port = sys.argv[1], int(sys.argv[2])
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.server_port))
        server_socket.listen()
        print(f"Listening on {(self.host, self.server_port)}")
        server_socket.setblocking(False)
        sel.register(server_socket, selectors.EVENT_READ, data=None)

        def accept_wrapper(sock):
            conn, addr = sock.accept()  # Should be ready to read
            print(f"Accepted connection from {addr}")
            conn.setblocking(False)
            data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
            socket_events = selectors.EVENT_READ | selectors.EVENT_WRITE
            sel.register(conn, socket_events, data=data)

        def service_connection(service_key, service_mask):
            sock = service_key.fileobj
            data = service_key.data
            if service_mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)  # Should be ready to read
                if recv_data:
                    data.outb += recv_data
                else:
                    print(f"Closing connection to {data.addr}")
                    sel.unregister(sock)
                    sock.close()
            if mask & selectors.EVENT_WRITE:
                if data.outb:
                    print(f"Echoing {data.outb!r} to {data.addr}")
                    sent = sock.send(data.outb)  # Should be ready to write
                    data.outb = data.outb[sent:]

        try:
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            sel.close()


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