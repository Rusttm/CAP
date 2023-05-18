import time

from SocSrv.SocketMainClass import SocketMainClass
from socket import socket, AF_INET, SOCK_STREAM
import socket
import datetime
import pickle

socket.setdefaulttimeout(10)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # client_socket.setblocking(False)

    client_socket.timeout
    client_socket.connect((socket.gethostbyname(socket.gethostname()), 1977))
    try:
        hello_msg = {"from": "main", "to": "server", "data": f"Main client starts1"}
        client_socket.sendall(pickle.dumps(hello_msg))
    except BlockingIOError:
        print("wait for blocking error 1")
            # pass
    while True:
        try:
            data = client_socket.recv(1024)
            print(pickle.loads(data))
        except BlockingIOError:
            print("wait for blocking error 2")
        except TimeoutError:
            print("data is not receiving")
        else:
            time.sleep(30)
            msg = pickle.loads(data)
            msg["to"], msg["from"] = msg["from"], msg["to"]
            data = pickle.dumps(msg)
            client_socket.sendall(data)




