import sys
import os
import platform

sys_os = platform.platform()
APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_PATH)
sys.path.append(MODULE_PATH)
print(f"Current project path: {APP_PATH}, module {MODULE_PATH} added to System: {sys_os}")

import time
import datetime
from SocSrv.SocketMainClass import SocketMainClass
from SocSrv.ContSC.ContSCServer import ContSCServer
from SocSrv.ContSC.ContSCClientAdmin import ContSCClientAdmin


try:
    SOC_PING_TIME = os.environ["SOC_PING_TIME"]
except:
    os.environ["SOC_PING_TIME"] = "3600"  # every hour


class SocSrvMain(SocketMainClass):
    """ main class for Socket Service Server and Admin Client"""
    
    def __init__(self):
        super().__init__()
        self.main()

    def main(self):
        self.server = ContSCServer()
        print(f"Socket Server started at {time.ctime()}")
        self.logger.debug(f"{__class__.__name__} started 'server' socket service")
        time.sleep(3)
        self.admin_client = ContSCClientAdmin()
        print(f"Admin socket client started at {time.ctime()}")
        self.logger.debug(f"{__class__.__name__} started 'admin' socket service")


if __name__ == '__main__':

    socket_service = SocSrvMain()
    # socket_service.main()
    while True:
        # time.sleep(86400) # everyday
        time.sleep(int(os.environ["SOC_PING_TIME"]))
        current_time = datetime.datetime.now().strftime('%y:%m:%d :%H:%M:%S')
        print(f"incoming messages on server {socket_service.server.get_socserver_incomings()}")
        print(f"outgoing messages on server {socket_service.server.get_socserver_outgoins()}")
        print(f"incoming messages on admin {socket_service.admin_client.get_all_incoming_msgs()}")
        print(f"outgoing messages on admin {socket_service.admin_client.get_all_outgoing_msgs()}")
        msg_dict = dict({"to": "telegram", "from": "admin", "at": current_time, "text": "Hi telegram msg from admin"})
        socket_service.admin_client.send_socket_msg_dict(msg_dict)
