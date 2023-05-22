# from https://steelkiwi.com/blog/working-tcp-sockets/
import time

from SocSrv.SocketMainClass import SocketMainClass
import pickle
import select
import socket
import queue
from threading import Thread


class ConnSCServer(SocketMainClass):
    """ starts socket server"""
    host = 'localhost'
    server_port = 1977
    buffer = 1024
    message_queues_socket_data_dict = {}
    """ dictionary {_socket: msg.data, client_socket:  msg.data}"""
    incoming_msg_queue = []
    outgoing_msg_queue = []
    """ dictionary {"from": "user_name", "to":"telegram", 'text':'message text',"""
    incoming_msg_list = []
    """ all income messages list"""
    outgoing_msg_list = []
    """ all outgunned messages list"""
    outputs_sockets = []
    inputs_sockets = []
    clients_name_socket_dict = dict()
    """ dictionary {"server": client_socket, "telegram": client_socket,"""
    clients_socket_name_dict = dict()
    """ dictionary { client_socket : "server", client_socket: "telegram","""
    sockets_set_4select = set()
    """ dictionary {"server": client_socket, "telegram": client_socket,"""

    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.start_socket_server()
        Thread(target=self.listen_4receive_dict, args=[]).start()
        # Thread(target=self.listen_4receive_dict, args=[]).run()
        self.logger.debug(f"{__class__.__name__} server is listening port {self.server_port}")

    def start_socket_server(self):
        try:
            self.host = (socket.gethostname(), self.server_port)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # reuse address in OS after closing (0 - no timeout)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.setblocking(False)
            self.server_socket.bind(self.host)
            self.server_socket.listen(10)
            # self.inputs_sockets.append(self.server_socket)
            self.sockets_set_4select.add(self.server_socket)
            self.clients_socket_name_dict[self.server_socket] = "server"
            self.clients_name_socket_dict['server'] = self.server_socket
            self.logger.debug(f"{__class__.__name__} server initiated on {self.server_port}")
        except OSError as e:
            self.logger.debug(f"{__class__.__name__} server address is not reachable, error: {e}")

    def listen_4receive_dict(self):
        try:
            self.logger.debug(f"{__class__.__name__} server fetching clients in select")
            while 1:
                # receive lists of sockets ready for read/write/error
                all_sockets_list = list(self.sockets_set_4select)
                # sockets_readable, sockets_sendable, sockets_for_except = select.select(self.inputs_sockets,
                # self.outputs_sockets,
                # self.inputs_sockets)
                sockets_readable, sockets_sendable, sockets_for_except = select.select(all_sockets_list,
                                                                                       all_sockets_list,
                                                                                       all_sockets_list)

                """ 
                sockets_readable - sockets that already have a msg and waiting you to get it
                sockets_sendable - sockets that ready to receive msg and waiting you to send it
                """
                for _socket in sockets_readable:
                    # select only sockets for read
                    if _socket == self.server_socket:  # primary choose server ready to read
                        client_socket, addr = self.server_socket.accept()
                        client_socket.setblocking(False)
                        # self.inputs_sockets.append(client_socket)
                        self.sockets_set_4select.add(client_socket)
                        # make empty message from server???
                        self.message_queues_socket_data_dict[_socket] = queue.Queue
                    else:  # looks new clients (not server) ready to read
                        self.incoming_msg_handler(_socket)
                        # print(f"server read msg from {self.clients_socket_name_dict[_socket]} socket ")

                for _socket in sockets_sendable:
                    self.outgoing_msg_handler(_socket)
                    # print(f"server send msg to {self.clients_socket_name_dict[_socket]} socket ")

                for _socket in sockets_for_except:
                    """ remove sockets with errors from sockets_list and clients_dict """
                    # self.inputs_sockets.remove(_socket)
                    if _socket in self.outputs_sockets:
                        # self.outputs_sockets.remove(_socket)
                        self.sockets_set_4select.remove(_socket)
                        self.logger.error(f"{__class__.__name__} socket was removed cause exception")
                    try:
                        _socket.close()
                        del self.message_queues_socket_data_dict[_socket]
                    except Exception as e:
                        self.logger.error(f"{__class__.__name__} cant close socket and remove it from queue error: {e}")
        except KeyboardInterrupt:
            print("Server shutting down by administrator")
            self.logger.info("Socket Server was cancelled by admin")
            return True

    def incoming_msg_handler(self, _socket):
        try:
            # get new message
            # data = _socket.recv(self.buffer)
            data = b''
            while True:
                request = _socket.recv(self.buffer)
                data += request
                if len(request) < self.buffer:
                    break
            if data:
                # change reply message
                msg = pickle.loads(data)
                # print(f"incoming msg: {msg}")
                self.logger.info(f"{__class__.__name__} receive msg: {msg}")
                self.incoming_msg_list.append(msg)
                # make dictionary client:socket like {"server":_socket}
                self.clients_name_socket_dict[msg['from']] = _socket
                self.clients_socket_name_dict[_socket] = msg['from']
                # handling initial msg with request to server
                if msg["to"] == "server":
                    self.server_msg_handler(msg=msg, _socket=_socket)
                else:
                    self.forward_msg_handler(msg=msg, _socket=_socket)
            else:
                """ if msg empty delete clients from sockets_list and clients_dict"""
                self.empty_msg_handler(_socket)
                # print("client send empty request")
        except ConnectionResetError as e:
            _socket.close()
            self.sockets_set_4select.remove(_socket)
            self.logger.warning(f"client connection with socket lost, error: {e}")

    def outgoing_msg_handler(self, _socket):
        # handling outgoing messages
        try:
            # client_name = self.clients_socket_name_dict[_socket]
            # is _socket in queue with ready for send messages
            if _socket in self.message_queues_socket_data_dict.keys():
                next_msg_data = self.message_queues_socket_data_dict[_socket]
                _socket.send(next_msg_data)
                msg = pickle.loads(next_msg_data)
                self.logger.info(f"{__class__.__name__} send msg to: {msg}")
                try:
                    # delete data after sending msg
                    del self.message_queues_socket_data_dict[_socket]
                except Exception as e:
                    self.logger.warning(f"{__class__.__name__} cant find _socket or msg in queues error {e}")
        except queue.Empty as e:
            # if msg is empty - remove from select outgoing sockets list
            # self.outputs_sockets.remove(_socket)
            # self.sockets_set_4select.remove(_socket)  # why?
            self.logger.info(f"{__class__.__name__} cant read data for next empty msg error: {e}")
        except Exception as e:
            self.logger.info(f"{__class__.__name__} cant read data for next msg error: {e}")

    def empty_msg_handler(self, _socket):
        """if receive empty msg"""
        # try to find client name
        try:
            from_name = "unknown"
            for client_name, __socket in self.clients_name_socket_dict.items():
                if __socket == _socket:
                    from_name = client_name
            self.logger.info(f"{__class__.__name__} receive empty msg from {from_name}")
            # if _socket in self.outputs_sockets:
            if _socket in self.sockets_set_4select:
                self.logger.debug(f"{__class__.__name__} server interrupt client msg is null")
                # no msg - no answer reject client from outgoing select list
                # self.outputs_sockets.remove(_socket)
                # if from_name == "unknown":
                self.sockets_set_4select.remove(_socket)  # dont know why i must to del this socket

            if _socket in self.message_queues_socket_data_dict.keys():
                del self.message_queues_socket_data_dict[_socket]
            _socket.close()  # close socket
            self.logger.info(f"{__class__.__name__} close socket from {from_name}")
            # empty msg then remove from select input sockets
            # self.inputs_sockets.remove(_socket)
            # if from_name == "unknown":
            #     self.sockets_set_4select.remove(_socket)  # dont know why i must to del this socket
            #     _socket.close()  # close socket
            #     self.logger.info(f"{__class__.__name__} close socket from {from_name}")
            #     try:
            #         del self.message_queues_socket_data_dict[_socket]  # remove from dict
            #     except Exception as e:
            #         # print(f"cant remove _socket from message_queues error: {e}")
            #         self.logger.error(f"{__class__.__name__} cant remove _socket from message_queues error: {e}")
        except Exception as e:
            self.logger.error(f"{__class__.__name__} cant handling empty msg error: {e}")

    def server_msg_handler(self, msg, _socket):
        # if msg for server and registering msgs
        msg["to"], msg["from"] = msg["from"], msg["to"]
        msg['text'] = f"{time.ctime()} request received: {msg['text']}"
        data = pickle.dumps(msg)
        # make reply to client in queue socket:msg
        self.message_queues_socket_data_dict[_socket] = data

    def forward_msg_handler(self, msg, _socket):
        # append to msgs queue list
        self.incoming_msg_queue.append(msg)
        # if forwarding message
        to_client = msg['to']
        try:
            # print(f"try to send '{to_client}'")
            # take socket of recipient from dict client_name:socket
            client_socket = self.clients_name_socket_dict[to_client]
            # append this msg to queue for outgoing msgs
            self.outgoing_msg_queue.append(msg)
            self.outgoing_msg_list.append(msg)
            data = pickle.dumps(msg)
            # put data in dictionary socket:data
            # if already have data
            temp_data = self.message_queues_socket_data_dict.get(client_socket, b'')
            self.message_queues_socket_data_dict[client_socket] = temp_data + data
            # and put socket in outgoing for select checking
            # if _socket not in self.outputs_sockets:
            #     self.outputs_sockets.append(client_socket)
        except KeyError as e:
            # print(f"client's '{to_client}' socket closed")
            self.logger.error(f"client '{to_client}' not online error: {e}")


if __name__ == '__main__':
    connector = ConnSCServer()
    print("Server runs!")
