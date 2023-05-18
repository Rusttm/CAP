# from https://steelkiwi.com/blog/working-tcp-sockets/
from SocSrv.SocketMainClass import SocketMainClass
import pickle
import select, socket, sys, queue
import logging

class ConnSCServerUDP(SocketMainClass):
    """ starts socket server"""
    host = 'localhost'
    server_port = 1977
    client_tg_port = 1978
    server_socket = None
    buffer = 1024
    sockets_list = []
    message_queues = {}
    """ dictionary {_socket: msg.data, client_socket:  msg.data}"""
    incoming_msg_queue = []
    outgoing_msg_queue = []
    header_length = 10
    outputs_sockets = []
    inputs_sockets = []
    clients_name_dict = dict()
    """ dictionary {"server": client_socket, "telegram": client_socket,"""
    # tcp_udp_soc_type = "TCP" #or "UDP"
    tcp_udp_soc_type = "UDP"
    def __init__(self):
        super().__init__()
        self.start_socket_server()
        if self.tcp_udp_soc_type == "TCP":
            self._soc_type = socket.SOCK_STREAM
        else:
            self._soc_type = socket.SOCK_DGRAM

    def start_socket_server(self):
        self.host = (socket.gethostname(), self.server_port)
        if self.tcp_udp_soc_type == "TCP":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse address in OS after closing (0 - no timeout)
        self.server_socket.bind(self.host)
        # self.server_socket.listen(5)
        self.inputs_sockets.append(self.server_socket)
        self.logger.debug(f"{__class__.__name__} server initiated and listening port {self.server_port}")

    # version for dictionary
    def get_client_msg_dict(self, client_socket: socket.socket):
        """ receive and decoding clients dictionaries"""
        self.logger.debug(f"{__class__.__name__} server extracts clients msg from client_socket")
        # receive dictionary
        try:
            data = client_socket.recv(self.buffer)
            msg = pickle.loads(data)
            print(f"you have message: {msg}")
            return msg
        except Exception as e:
            self.logger.error(f"{__class__.__name__} server error: {e}")
            return False
    def decode_data_2dict(self, data):
        return pickle.loads(data)
    def listen_4receive_dict(self):
        try:
            self.logger.debug(f"{__class__.__name__} server fetching clients in select")
            inputs = self.inputs_sockets
            outputs = self.outputs_sockets
            while 1:
                # receive lists of sockets ready for read/write/error
                client_for_read, client_for_send, client_for_except = select.select(inputs, outputs, inputs)
                """ client_for_read - clients sockets that already receive msg and ready to read it"""
                for _socket in client_for_read:
                    # select only sockets for read
                    if _socket == self.server_socket:  # primary choose server ready to read
                        # client_socket, addr = self.server_socket.accept()
                        # client_socket.setblocking(0)
                        # inputs.append(client_socket)
                        _socket.setblocking(0)
                        inputs.append(_socket)
                        self.message_queues[_socket] = queue.Queue

                    else:  # looks new clients (not server) ready to read
                        # get new message
                        data = _socket.recv(1024)
                        if data:
                            print(self.decode_data_2dict(data=data))
                            # change reply message
                            msg = pickle.loads(data)
                            self.incoming_msg_queue.append(msg)
                            # first msg with request to server
                            self.clients_name_dict[msg['from']] = _socket
                            if msg["to"] == "server":
                                # if msg for server and registerring msgs
                                msg["to"], msg["from"] = msg["from"], msg["to"]
                                msg['text'] = "request recieved"
                                data = pickle.dumps(msg)
                                self.message_queues[_socket] = data
                                if _socket not in outputs:
                                    outputs.append(_socket)
                            else:
                                # if forward message
                                if self.outgoing_msg_queue:
                                    for msg in self.outgoing_msg_queue:
                                        to_client = msg['to']
                                        client_socket = self.clients_name_dict[to_client]
                                        next_msg = pickle.dumps(msg)
                                        self.message_queues[client_socket] = next_msg
                        else:
                            """ if msg empty delete clients from sockets_list and clients_dict"""
                            if _socket in outputs:
                                self.logger.debug(f"{__class__.__name__} server interrupt client msg is null")
                                outputs.remove(_socket)
                            inputs.remove(_socket)
                            _socket.close() # close socket
                            try:
                                del self.message_queues[_socket]  # remove from dict
                            except:
                                pass
                for _socket in client_for_send:
                    try:
                        next_msg = self.message_queues[_socket]
                    except queue.Empty:
                        outputs.remove(_socket)
                    else:
                        _socket.send(next_msg)
                        # test
                        outputs.remove(_socket)

                for _socket in client_for_except:
                    """ remove sockets with errors from sockets_list and clients_dict """
                    inputs.remove(_socket)
                    if _socket in outputs:
                        outputs.remove(_socket)
                    _socket.close()
                    del self.message_queues[_socket]
        except KeyboardInterrupt:
            print("Server shutting down by administrator")
            self.logger.info("Socket Server was cancelled by admin")
            return True


if __name__ == '__main__':
    connector = ConnSCServerUDP()
    # my_dictionary = dict({"module": "telegram", "data": {"from": "57685837", "text": "hello telegram"}})
    # print(connector.send_2client_dict(my_dictionary))
    connector.listen_4receive_dict()
