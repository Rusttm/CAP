import asyncio
import time
from threading import Thread

from SocSrv.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM
import socket
import datetime
import pickle

class ConnSCClientMain(SocketMainClass):
    incoming_msg_queue = []
    outgoing_msg_queue = []
    server_port = 1977
    server_host = 'localhost'
    client_name = "telegram"

    def __init__(self, client_name=None, server_port=None, server_host=None):
        super().__init__()
        if client_name:
            self.client_name = client_name
        if server_port:
            self.server_port = server_port
        if server_host:
            self.server_host = server_host
        else:
            self.server_host = socket.gethostbyname(socket.gethostname())
        self.outgoing_msg_queue.append({"to": "server", "text": f"{self.client_name} client starts"})
        self.outgoing_msg_queue.append(
            {"from": self.client_name, "to": "main", "text": f"{self.client_name} client starts"})

    def start_socket_client(self):
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
                            out_msg = {"from": self.client_name, "to": f"{msg_dict['to']}", "text": f"{msg_dict['text']}"}
                            # time.sleep(1)
                            client_socket.sendall(pickle.dumps(out_msg))
                            # self.outgoing_msg_queue.remove(msg_dict)
                    except BlockingIOError:
                        print("wait for blocking error 1")
                    try:
                        data = client_socket.recv(1024)
                    except BlockingIOError:
                        print("wait for blocking error 2")
                    except TimeoutError:
                        print(f"outgoing messages {self.outgoing_msg_queue}")
                        print(f"incoming messages {self.incoming_msg_queue}")
                        print("data is not receiving")
                    else:
                        # time.sleep(30)
                        msg = pickle.loads(data)
                        print(f"incoming message {msg}")
                        self.incoming_msg_queue.append(msg)

                        # msg["to"], msg["from"] = msg["from"], msg["to"]
                        # data = pickle.dumps(msg)
                        # client_socket.sendall(data)
        except KeyboardInterrupt:
            print("Bye - Bye")
            self.logger.info("Socket Server was interrupted by admin")
            return True
        except ConnectionRefusedError as e:
            print("no connection")
            self.logger.critical(f"Socket Server is not responding {e}")

    def send_dict_2client(self, to=None, msg_text=None):
        # print(f"add new message {self.outgoing_msg_queue}")
        # if not to and not msg_text:
        new_msg = {"from": self.client_name, "to": to, "text": msg_text}
        self.outgoing_msg_queue.append(new_msg)
        return True
        # return False


if __name__ == '__main__':
    connector = ConnSCClientMain()
    connector.start_socket_client()
    to = "main"
    msg_text = "it's again me"
    for i in range(5):
        time.sleep(3)
        msg_text = f"{i}: it's again me"
        connector.send_dict_2client(to=to, msg_text=msg_text)

    #
    # connector = ConnSCClientMain()
    # t1 = Thread(target=connector.start_socket_client, args=[]).start()
    #
    # print("all started")

    # connector.send_dict_2client(to=to, msg_text=msg_text)
    # # t2 = Thread(target=connector.send_dict_2client, args=(to, msg_text)).start()
    # # t2.run()
