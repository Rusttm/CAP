import time
import setup
from CAPMain.CAPMainClass import CAPMainClass


class Main(CAPMainClass):

    def __init__(self):
        super().__init__()
        self.socket_service = None
        self.telegram_service = None

    def start_socket_service(self):
        from SocSrv.SocSrvMain import SocSrvMain
        self.socket_service = SocSrvMain()

    def start_telegrambot_service(self):
        from API_Tbot.TGBotMain import TGBotMain
        self.telegram_service = TGBotMain()

    def main(self):
        self.start_socket_service()
        time.sleep(3)
        self.start_telegrambot_service()


if __name__ == '__main__':
    main_class = Main()
    main_class.main()
    for i in range(100):
        time.sleep(3600)
        now = time.ctime()
        msg_line = f"Hi telegram {i} msg from admin at {now}"
        main_class.socket_service.admin_client.send_socket_msg(to_user="telegram",
                                                               msg_text=msg_line)

    # msapi1 = ContCAPMS.ContCAPMS()
    # msapi1.get_cont_id()
    # msapi2 = ContCAPMS.ContCAPMS()
    # msapi3 = ContCAPMS.ContCAPMS()
    # rc = 1
    # try:
    #     # print("main()")
    #     rc = 0
    # except Exception as e:
    #     print('Error: %s' % e, file=sys.stderr)
    # sys.exit(rc)