import time

from SocSrv.SocketMainClass import SocketMainClass
from SocSrv.ContSC.ContSCServer import ContSCServer
from SocSrv.ContSC.ContSCClientAdmin import ContSCClientAdmin
from SocSrv.ContSC.ContSCClientTg import ContSCClientTg

class SocSrvMain(SocketMainClass):
    """ main class for Socket Service Server and Admin Client"""
    
    def __init__(self):
        super().__init__()


    def main(self):
        self.server = ContSCServer()
        time.sleep(3)
        self.admin_client = ContSCClientAdmin()



if __name__ == '__main__':
    socket_service = SocSrvMain()
    socket_service.main()
    for i in range(10):
        time.sleep(5)
        print(f"incoming messages on server {socket_service.server.get_socserver_incomings()}")
        print(f"outgoing messages on server {socket_service.server.get_socserver_outgoins()}")
        print(f"incoming messages on admin {socket_service.admin_client.get_all_incoming_msgs()}")
        print(f"outgoing messages on admin {socket_service.admin_client.get_all_outgoing_msgs()}")
        socket_service.admin_client.send_socket_msg(to_user="telegram", msg_text="Hi telegram from admin")
