import time

from Pgsql.ContPgsql.ContPgsql import ContPgsql
from threading import Thread

class PgsqlMain(ContPgsql):
    socket_controller = None
    socket_name = "pgsql"
    outgoing_messages = [] # messages dictionary msg = {to_user=msg.get("to"), msg_text=msg.get("msg_text")}
    incoming_messages = []

    def __init__(self):
        super().__init__()

    def start_pgsql_socket_service(self):
        from Pgsql.PgsqlSocSrv.PgsqlSocSrvCont.ContPgsqlSocSrvClient import ContPgsqlSocSrvClient
        self.socket_controller = ContPgsqlSocSrvClient(client_name=self.socket_name)
        self.logger.debug(f"{__class__.__name__} started '{self.socket_name}' socket service")
        while True:
            time.sleep(2)
            try:
                # get new messages from server
                new_msg_list = self.socket_controller.get_all_incoming_msgs()
            except Exception as e:
                self.logger.critical(f"{__class__.__name__} doesn't work, {self.socket_name} socket client closed, error: {e}")
                break
            else:
                if self.outgoing_messages:
                    for msg in self.outgoing_messages:
                        self.socket_controller.send_socket_msg(to_user=msg.get("to"), msg_text=msg.get("msg_text"))
                for msg in new_msg_list:
                    self.incoming_messages.append(msg)
                    print(f"received new msg: {msg}")

    def send_msg_2telegram(self, msg_text=None):
        if self.socket_controller:
            if msg_text:
                msg = dict({"to": "telegram", "from": self.socket_name, "msg_text": msg_text})
                self.outgoing_messages.append(msg)
                return True
        else:
            return False

    def send_service_msg_to(self, to_user="admin", msg_text=None):
        if self.socket_controller:
            if msg_text:
                msg = dict({"to": to_user, "from": self.socket_name, "msg_text": msg_text})
                self.outgoing_messages.append(msg)
                return True
        else:
            return False

    def pgsql_db_init(self):
        from.ContPgsql.DatabaseInit.ContPgsqlInitMain import ContPgsqlInitMain
        init_db_controller = ContPgsqlInitMain().initial_base_main()
        self.logger.debug(f"{__file__.__name__} init database {init_db_controller}")

    def pgsql_db_updater(self):
        from Pgsql.ContPgsql.ContPgsqlUpdater import ContPgsqlUpdater
        start_updates_controller = ContPgsqlUpdater().update_all_report_tables()
        self.logger.debug(f"{__file__.__name__}  start_updates {start_updates_controller}")
        return start_updates_controller

    def main_pgsql(self):
        try:
            Thread(target=self.start_pgsql_socket_service, args=[]).start()
            print(f"{self.socket_name} socket client started at {time.ctime()}")
        except Exception as e:
            print(f"{self.socket_name} cant run socket client error: {e}")
            self.logger.error(f"{__file__.__name__} cant run socket service error: {e}")
        self.pgsql_db_init()
        self.send_service_msg_to(to_user="telegram", msg_text=f"message from database initiated")
        while True:
            result_updater_messages = self.pgsql_db_updater()
            self.outgoing_messages.append(result_updater_messages)
            time.sleep(3600)


if __name__ == '__main__':
    controller = PgsqlMain()
    controller.main_pgsql()
    print("pgsql service is working ...")
    controller.send_msg_2telegram(msg_text=f"Hello, everybody, iam spam")
