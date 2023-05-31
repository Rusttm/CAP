import time
from Pgsql.PgsqlMainClass import PgsqlMainClass
from Pgsql.ContPgsql.ContPgsql import ContPgsql
from threading import Thread

class PgsqlMain(PgsqlMainClass):
    socket_controller = None
    socket_name = "pgsql"
    outgoing_messages = [] # messages dictionary msg = {to_user=msg.get("to"), msg_text=msg.get("msg_text")}
    incoming_messages = []
    update_period = 3600
    base_initiated = False

    def __init__(self):
        super().__init__()
        self.main_pgsql()

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
                    for msg in self.get_outgoing_messages():
                        try:
                            self.socket_controller.send_socket_msg(to_user=msg.get("to"), msg_text=msg.get("msg_text"))
                        except AttributeError as e:
                            self.logger.error("unknown type of message, it should be dictionary!")
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

    def get_outgoing_messages(self):
        out_msgs = self.outgoing_messages
        self.outgoing_messages = []
        return out_msgs

    def pgsql_db_init(self):
        from Pgsql.ContPgsql.DatabaseInit.ContPgsqlInitMain import ContPgsqlInitMain
        self.send_msg_2telegram("start initiating databases")
        init_db_controller = ContPgsqlInitMain().initiate_bases()
        self.logger.debug(f"{__class__.__name__} init database {init_db_controller}")
        self.send_msg_2telegram("databases initiated")
        self.base_initiated = True

    def pgsql_db_updater(self):
        from Pgsql.ContPgsql.ContPgsqlUpdater import ContPgsqlUpdater
        self.send_msg_2telegram("start updating databases")
        self.logger.debug(f"{__class__.__name__}  start_updates report tables")
        start_updates_controller = ContPgsqlUpdater().update_all_report_tables()
        self.logger.debug(f"{__class__.__name__}  report tables updated {start_updates_controller}")
        self.send_msg_2telegram("databases updated")
        return start_updates_controller

    def pgsql_db_updater_loop(self):
        from Pgsql.ContPgsql.ContPgsqlUpdater import ContPgsqlUpdater
        self.send_msg_2telegram("start updating databases")
        self.logger.debug(f"{__class__.__name__}  start_updates report tables")
        updater_controller = ContPgsqlUpdater()
        while True:
            # result_updater_messages = self.pgsql_db_updater()
            # self.send_msg_2telegram(f"result: {result_updater_messages}")
            start_updates_controller = updater_controller.update_all_report_tables()
            self.send_msg_2telegram(f"result: {start_updates_controller}")
            time.sleep(self.update_period)

    def main_pgsql(self):
        try:
            Thread(target=self.start_pgsql_socket_service, args=[]).start()
            print(f"{self.socket_name} socket client started at {time.ctime()}")
        except Exception as e:
            print(f"{self.socket_name} cant run socket client error: {e}")
            self.logger.error(f"{__class__.__name__} cant run socket service error: {e}")

        self.pgsql_db_init()

        try:
            Thread(target=self.pgsql_db_updater_loop(), args=[]).start()
            print(f"{self.socket_name} updater started at {time.ctime()}")
        except Exception as e:
            print(f"{self.socket_name} cant run updater error: {e}")
            self.logger.error(f"{__class__.__name__} cant run updater error: {e}")



if __name__ == '__main__':
    controller = PgsqlMain()
    controller.main_pgsql()
    print("pgsql service is working ...")
    controller.send_msg_2telegram(msg_text=f"Hello, everybody, iam pgsql spam")
