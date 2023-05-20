# from https://steelkiwi.com/blog/working-tcp-sockets/
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
    message_queues = {}
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
    clients_name_dict = dict()
    """ dictionary {"server": client_socket, "telegram": client_socket,"""

    def __init__(self):
        super().__init__()
        self.server_socket = None
        self.start_socket_server()
        Thread(target=self.listen_4receive_dict, args=[]).start()
        self.logger.debug(f"{__class__.__name__} server is listening port {self.server_port}")

    def start_socket_server(self):
        try:
            self.host = (socket.gethostname(), self.server_port)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reuse address in OS after closing (0 - no timeout)
            self.server_socket.bind(self.host)
            self.server_socket.listen(5)
            self.inputs_sockets.append(self.server_socket)
            self.logger.debug(f"{__class__.__name__} server initiated on {self.server_port}")
        except OSError as e:
            self.logger.debug(f"{__class__.__name__} server address is not reachable, error: {e}")
            raise e

    def get_client_msg_dict(self, client_socket: socket.socket):
        """ receive msg data from socket and return decoded msg"""
        self.logger.debug(f"{__class__.__name__} server extracts clients msg from client_socket")
        # receive dictionary
        try:
            data = client_socket.recv(self.buffer)
            msg = pickle.loads(data)
            # print(f"you have message: {msg}")
            self.logger.debug(f"{__class__.__name__} server got msg: {msg}")
            return msg
        except Exception as e:
            self.logger.error(f"{__class__.__name__} server error: {e}")
            return False

    def outgoing_msg_handler(self, _socket):
        # handling outgoing messages
        try:
            next_msg = self.message_queues[_socket]
        except queue.Empty:
            # if msg is empty - remove from select outgoing sockets list
            self.outputs_sockets.remove(_socket)
        else:
            _socket.send(next_msg)
            msg = pickle.loads(next_msg)
            # print(f"message from {msg['from']} to {msg['to']} was send by server ")
            self.logger.info(f"{__class__.__name__} send msg: {msg}")
            # after sending remove socket from select outgoing sockets
            self.outputs_sockets.remove(_socket)
            try:
                self.outgoing_msg_queue.remove(msg)
                # append to msgs queue list
                self.incoming_msg_queue.remove(msg)
            except Exception as e:
                self.logger.warning(f"{__class__.__name__} cant find msg: {msg} in queues")

    # def outgoing_msg_handler

    def incoming_msg_handler(self, _socket):
        # get new message
        data = _socket.recv(1024)
        if data:
            # change reply message
            msg = pickle.loads(data)
            # print(f"incoming msg: {msg}")
            self.logger.info(f"{__class__.__name__} receive msg: {msg}")
            self.incoming_msg_list.append(msg)
            # make dictionary client:socket like {"server":_socket}
            self.clients_name_dict[msg['from']] = _socket
            # handling initial msg with request to server
            if msg["to"] == "server":
                # if msg for server and registering msgs
                msg["to"], msg["from"] = msg["from"], msg["to"]
                msg['text'] = f"request received: {msg['text']}"
                data = pickle.dumps(msg)
                # make reply to client in queue socket:msg
                self.message_queues[_socket] = data
                # append socket in output list for select to checking this socket for send
                if _socket not in self.outputs_sockets:
                    self.outputs_sockets.append(_socket)
            else:
                # append to msgs queue list
                self.incoming_msg_queue.append(msg)
                # if forwarding message
                to_client = msg['to']
                try:
                    # print(f"try to send '{to_client}'")
                    # take socket of recipient from dict client_name:socket
                    client_socket = self.clients_name_dict[to_client]
                    # append this msg to queue for outgoing msgs
                    self.outgoing_msg_queue.append(msg)
                    self.outgoing_msg_list.append(msg)
                    data = pickle.dumps(msg)
                    # put data in dictionary socket:data
                    self.message_queues[client_socket] = data
                    # and put socket in outgoing for select checking
                    if _socket not in self.outputs_sockets:
                        self.outputs_sockets.append(client_socket)
                except KeyError as e:
                    # print(f"client's '{to_client}' socket closed")
                    self.logger.error(f"client '{to_client}' not online error: {e}")
        else:
            """ if msg empty delete clients from sockets_list and clients_dict"""
            # print("client send empty request")
            # try to find client name
            try:
                from_name = "unknown"
                for client_name, __socket in self.clients_name_dict.items():
                    if __socket == _socket:
                        from_name = client_name
                        break
                self.logger.info(f"{__class__.__name__} receive empty msg from {from_name}")
                if _socket in self.outputs_sockets:
                    self.logger.debug(f"{__class__.__name__} server interrupt client msg is null")
                    # no msg - no answer reject client from outgoing select list
                    self.outputs_sockets.remove(_socket)
                # empty msg then remove from select input sockets
                self.inputs_sockets.remove(_socket)
                _socket.close()  # close socket
                self.logger.info(f"{__class__.__name__} close socket from {from_name}")
                try:
                    del self.message_queues[_socket]  # remove from dict
                except Exception as e:
                    # print(f"cant remove _socket from message_queues error: {e}")
                    self.logger.error(f"{__class__.__name__} cant remove _socket from message_queues error: {e}")
            except Exception as e:
                self.logger.error(f"{__class__.__name__} cant handling empty msg error: {e}")

    def listen_4receive_dict(self):
        try:
            self.logger.debug(f"{__class__.__name__} server fetching clients in select")
            while 1:
                # receive lists of sockets ready for read/write/error
                sockets_readable, sockets_sendable, sockets_for_except = select.select(self.inputs_sockets, self.outputs_sockets, self.inputs_sockets)
                """ 
                sockets_readable - sockets that already have a msg and waiting you to get it
                sockets_sendable - sockets that ready to receive msg and waiting you to send it
                """
                for _socket in sockets_readable:
                    # select only sockets for read
                    if _socket == self.server_socket:  # primary choose server ready to read
                        client_socket, addr = self.server_socket.accept()
                        client_socket.setblocking(False)
                        self.inputs_sockets.append(client_socket)
                        # make empty message from server???
                        self.message_queues[_socket] = queue.Queue
                    else:  # looks new clients (not server) ready to read
                        self.incoming_msg_handler(_socket)

                for _socket in sockets_sendable:
                    self.outgoing_msg_handler(_socket)

                for _socket in sockets_for_except:
                    """ remove sockets with errors from sockets_list and clients_dict """
                    self.inputs_sockets.remove(_socket)
                    if _socket in self.outputs_sockets:
                        self.outputs_sockets.remove(_socket)
                    try:
                        _socket.close()
                        del self.message_queues[_socket]
                    except Exception as e:
                        self.logger.error(f"{__class__.__name__} cant close socket and remove it from queue error: {e}")
        except KeyboardInterrupt:
            print("Server shutting down by administrator")
            self.logger.info("Socket Server was cancelled by admin")
            return True


if __name__ == '__main__':
    connector = ConnSCServer()
    print("Server runs!")

