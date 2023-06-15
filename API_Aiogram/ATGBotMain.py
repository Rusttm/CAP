import time

from API_Aiogram.ContATGbot.ContATGBot import ContATGBot
from threading import Thread

class ATGBotMain(ContATGBot):

    def __init__(self):
        super().__init__()
        Thread(target=self.start_tg_socket_service, args=[]).start()
        print(f"Telegram socket client started at {time.ctime()}")
        self.start_telegrambot()

    def start_tg_socket_service(self):
        from API_Aiogram.ContATGbot.ContATGBotSocSrvClient import ContATGBotSocSrvClient
        self.socket_controller = ContATGBotSocSrvClient()
        self.logger.debug(f"{__class__.__name__} started 'telegram' socket service")
        while True:
            time.sleep(2)
            try:
                new_msg_list = self.socket_controller.get_all_incoming_msgs()
            except Exception as e:
                self.logger.critical(f"{__class__.__name__} doesn't work, socket client closed, error: {e}")
                break
            else:
                for msg in new_msg_list:
                    self.send_service_msg(msg=msg)

    # def start_tg_aiogram_api(self):
    #     self.start_telegrambot()


if __name__ == '__main__':
    controller = ATGBotMain()
    print("bot is working ...")
    # controller.send_spam_msg(msg=f"Hello, everybody, iam spam")
    # controller.start_telegrambot()