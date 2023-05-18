from SocSrv.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM
import socket
import datetime
import pickle


class ConnSCClientMain(SocketMainClass):
    """ client for main module"""
    client_name = "main"
    """ name of socket client"""
    server_port = 1977
    """ server port"""
    server_host = '127.0.0.1'
    """ server host"""
    buffer = 1024  # bytes
    """ length of received data"""
    conn_num = 5
    """ tuple (server host, server port)"""
    server_msgs_list = []
    """ list of messages received from server"""

    def __init__(self):
        super().__init__()
        # self.server_host = socket.gethostname()
        self.HOST = (self.server_host, self.server_port)

    def start_socket_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # set buffer to not blocking during the sending information
            client_socket.setblocking(0)
            client_socket.connect(self.HOST)
            self.logger.debug(f"{__class__.__name__} client connect to server {self.HOST} for send dict")
            hello_msg = {"from": f"{self.client_name}", "to": "server", "data": f"Main client starts at {datetime.now()}"}
            client_socket.sendall(pickle.dumps(hello_msg))
            data = client_socket.recv(self.buffer)
            print(pickle.loads(data))


if __name__ == '__main__':
    connector = ConnSCClientMain()
    # connector.send_dict_2server(to="telegram", data="Hi from Main module")
    connector.start_socket_client()
    # connector.recv_dict_from_server()