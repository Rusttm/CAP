import time
from threading import Thread
from SocSrv.SocketMainClass import SocketMainClass
from socket import socket
import socket
import pickle


class ConnSCClientMainClass(SocketMainClass):
    """ main class for socket clients
    for new child class please rename 'client_name' """
    incoming_msg_list = [] # list for all incoming msg
    outgoing_msg_list = [] # list for all outgoing msg
    outgoing_msg_queue = []
    server_port = 1977
    server_host = 'localhost'
    # client_name = "main"

    def __init__(self, name=None):
        super().__init__()
        self.client_name = name
        # if server_port:
        #     self.server_port = server_port
        if not self.server_host:
            self.server_host = socket.gethostbyname(socket.gethostname())
        self.server_host = socket.gethostbyname(socket.gethostname())
        server_start_msg = {"from": self.client_name, "to": "server", "text": f"{self.client_name} client starts"}
        self.outgoing_msg_queue.append(server_start_msg)
        itself_start_msg =  {"from": self.client_name, "to": self.client_name, "text": f"{self.client_name} self replying"}
        self.outgoing_msg_queue.append(itself_start_msg)
        Thread(target=self.__start_socket_client, args=[]).start()

    def set_client_name(self, name=None):
        if name:
            self.client_name = name

    def __start_socket_client(self):
        try:
            # socket.setdefaulttimeout(10)
            # socket.timeout(1)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # client_socket.setblocking(False)
                # client_socket.timeout
                client_socket.connect((self.server_host, self.server_port))
                while True:
                    try:
                        if self.outgoing_msg_queue:
                            msg_dict = self.outgoing_msg_queue.pop(0)
                            client_socket.sendall(pickle.dumps(msg_dict))
                            self.outgoing_msg_list.append(msg_dict)
                            self.logger.info(f"{self.client_name} send msg: {msg_dict}")
                    except BlockingIOError as e:
                        self.logger.error(f"{self.client_name} blocking error in sendall: {e}")
                    try:
                        data = client_socket.recv(1024)
                    except BlockingIOError as e:
                        self.logger.error(f"{self.client_name} blocking error in receive: {e}")
                    except TimeoutError as e:
                        self.logger.error(f"{self.client_name} timeout error in receive: {e}")
                    else:
                        # time.sleep(3)
                        msg = pickle.loads(data)
                        self.logger.info(f"{self.client_name} receive msg: {msg}")
                        self.incoming_msg_list.append(msg)
        except KeyboardInterrupt:
            self.logger.info("Socket Server was interrupted by admin")
        except ConnectionRefusedError as e:
            self.logger.critical(f"Socket Server is not responding {e}")
        except BlockingIOError as e:
            self.logger.critical(f"IOError -Socket Server is not responding {e}")

    def send_dict_2client(self, to=None, msg_text=None):
        if to:
            try:
                new_msg = {"from": self.client_name, "to": to, "text": msg_text}
                self.outgoing_msg_queue.append(new_msg)
            except Exception as e:
                self.logger.error(f"{self.client_name} can't add message: {e}")
        else:
            self.logger.error(f"{self.client_name} new message not specified 'to' receiver: {to}")

    def get_all_incoming_msgs(self):
        all_messages_list= self.incoming_msg_list
        self.incoming_msg_list = []
        self.logger.info(f"{self.client_name} erase all incoming messages")
        return all_messages_list

    def get_all_outgoing_msgs(self):
        all_messages_list= self.outgoing_msg_list
        self.outgoing_msg_list = []
        self.logger.info(f"{self.client_name} erase all outgoing messages")
        return all_messages_list

if __name__ == '__main__':
    client_name = "main"
    connector = ConnSCClientMainClass(name=client_name)
    to = "main"
    msg_text = "it's again me"
    connector.send_dict_2client(to=to, msg_text=msg_text)
    # t2 = Thread(target=connector.send_dict_2client, args=(to, msg_text)).start()  # if it is necessary to use threads
    print("client successfully started")
    time.sleep(3)
    print(f"full received messages list: {connector.get_all_incoming_msgs()}")
