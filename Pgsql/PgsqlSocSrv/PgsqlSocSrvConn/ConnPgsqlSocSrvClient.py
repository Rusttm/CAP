import time
from Pgsql.PgsqlSocSrv.PgsqlSocSrvConn.ConnPgsqlSocSrvMainClass import ConnPgsqlSocSrvMainClass


class ConnPgsqlSocSrvClient(ConnPgsqlSocSrvMainClass):
    """ socket client for telegram bot"""

    def __init__(self, client_name="pgsql"):
        super().__init__(client_name=client_name)


if __name__ == '__main__':
    connector = ConnPgsqlSocSrvClient(client_name="pgsql")
    to_user = "main"
    msg_text = f"Hi, {to_user}! This message from pgsql. "
    connector.send_dict_2client(to_user=to_user, msg_text=msg_text)
    print("client successfully started")
    time.sleep(3)
    print(f"full received messages list: {connector.get_all_incoming_msgs()}")