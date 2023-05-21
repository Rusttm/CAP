
from API_Tbot.TGBotMainClass import TGBotMainClass
import time
from threading import Thread
from socket import socket
import socket
import pickle


class ConnTGBotSocSrvMainClass(TGBotMainClass):
    """ main class for socket clients
    for new child class please rename 'client_name' """
    incoming_msg_list = []  # list for all incoming msg
    outgoing_msg_list = []  # list for all outgoing msg
    outgoing_msg_queue = []
    server_port = 1977
    server_host = 'localhost'
    buffer = 3072
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
        itself_start_msg = {"from": self.client_name, "to": self.client_name, "text": f"{self.client_name} self replying"}
        self.outgoing_msg_queue.append(itself_start_msg)
        Thread(target=self.start_socket_client, args=[]).start()
        # self.__start_socket_client()
    def set_client_name(self, name=None):
        if name:
            self.client_name = name

    def start_socket_client(self):
        try:
            socket.setdefaulttimeout(10)
            # socket.timeout(3)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # client_socket.setblocking(False)
                client_socket.timeout
                client_socket.connect((self.server_host, self.server_port))
                while True:
                    # print(f"queue length: {len(self.outgoing_msg_queue)}")
                    # time.sleep(1)
                    try:
                        if self.outgoing_msg_queue:
                            msg_dict = self.outgoing_msg_queue.pop(0)
                            client_socket.sendall(pickle.dumps(msg_dict))
                            # self.outgoing_msg_queue.remove(msg_dict)
                            self.outgoing_msg_list.append(msg_dict)
                            self.logger.info(f"{self.client_name} send msg: {msg_dict}")
                            # print(f"{self.client_name} send to {msg_dict['to']} msg: {msg_dict}")
                    except BlockingIOError as e:
                        self.logger.error(f"{self.client_name} blocking error in sendall: {e}")
                    try:
                        data = b''
                        while True:
                            request = client_socket.recv(self.buffer)
                            data += request
                            if len(request) < self.buffer:
                                break
                        msg_dict = pickle.loads(data)
                    except BlockingIOError as e:
                        self.logger.error(f"{self.client_name} blocking error in receive: {e}")
                    except TimeoutError as e:
                        self.logger.error(f"{self.client_name} timeout error in receive: {e}")
                    except EOFError as e:
                        self.logger.error(f"{self.client_name} data convert error in received msg: {e}")
                    else:
                        # time.sleep(3)

                        self.logger.info(f"{self.client_name} receive msg: {msg_dict}")
                        # print(f"{self.client_name} receive from {msg_dict['from']} msg: {msg_dict}")
                        self.incoming_msg_list.append(msg_dict)
        except KeyboardInterrupt:
            self.logger.info("Socket Server was interrupted by admin")
        except ConnectionRefusedError as e:
            self.logger.critical(f"Socket Server is not responding {e}")
        except BlockingIOError as e:
            self.logger.critical(f"IOError -Socket Server is not responding {e}")

    def send_dict_2client(self, to_user=None, msg_text=None):
        if to_user and msg_text:
            try:
                new_msg = {"from": self.client_name, "to": to_user, "text": msg_text}
                self.outgoing_msg_queue.append(new_msg)
                # print(f"added in queue {self.outgoing_msg_queue}")
                return True
            except Exception as e:
                self.logger.error(f"{self.client_name} can't add message: {e}")
        else:
            self.logger.error(f"{self.client_name} new message not specified 'to' receiver: {to_user}")
        return False

    def get_all_incoming_msgs(self):
        all_messages_list= self.incoming_msg_list
        self.incoming_msg_list = []
        # self.logger.debug(f"{self.client_name} erase all incoming messages")
        return all_messages_list

    def get_all_outgoing_msgs(self):
        all_messages_list= self.outgoing_msg_list
        self.outgoing_msg_list = []
        # self.logger.debug(f"{self.client_name} erase all outgoing messages")
        return all_messages_list

if __name__ == '__main__':
    client_name = "main"
    connector = ConnTGBotSocSrvMainClass(name=client_name)
    # Thread(target=connector.start_socket_client, args=[]).start()
    # connector.start_socket_client()
    connector.outgoing_msg_queue.append({'from': 'main', 'to': 'main', 'text': 'прощай немытая Россия'})
    to_user = "server"
    print(f"client {client_name} successfully started")
    for i in range(10):
        time.sleep(1)
        msg_text = f"msg No {i} it's again me {client_name}"
        send = connector.send_dict_2client(to_user=to_user, msg_text=msg_text)

