#~/cap_env/bin/python
import time

from CAPMain.CAPMainClass import CAPMainClass
import asyncio
import aioschedule

class Main(CAPMainClass):

    def __init__(self):
        super().__init__()
        # self.socket_service = None
        # self.telegram_service = None

    # def start_socket_service(self):
    #     from SocSrv.SocSrvMain import SocSrvMain
    #     self.socket_service = SocSrvMain()
    #
    # def start_telegrambot_service(self):
    #     from API_Tbot.TGBotMain import TGBotMain
    #     self.telegram_service = TGBotMain()
        # Thread(target=TGBotMain, args=[]).start()

    # def start_telegrambot_service(self):
    #     from API_Aiogram.TGBotMain import TGBotMain
    #     self.telegram_service = TGBotMain()


    # def start_api_db_updater(self):
    #     from Pgsql.PgsqlMain import PgsqlMain
    #     self.updater_service = PgsqlMain()

    async def start_db_updater(self, upd_msg):
        print(f"Запускаю {upd_msg} отчет")
        await asyncio.sleep(5)
        try:
            from PgsqlAlchemy.ModALUpdaters.ModALUpdater import ModALUpdater
            ModALUpdater().db_updater(period=upd_msg)
            await asyncio.sleep(1)
        except Exception as e:
            msg = f"Не смог запустить отчет {upd_msg}, ошибка: {e}"
            self.logger.error(msg)
            print(msg)
        else:
            msg = f"Отчет {upd_msg} записан"
            print(msg)


    def main(self):
        print("CAPService was not run, due to reconstruction")
        # self.start_socket_service()
        # time.sleep(3)
        # self.start_telegrambot_service()
        # time.sleep(3)
        # self.start_api_db_updater()
    async def main_async(self, count=0):
        await asyncio.sleep(2)
        print("You run asyncio CAP services")
        upd_msg = f"daily"
        aioschedule.every().day.at("21:25").do(self.start_db_updater, upd_msg=upd_msg)
        upd_msg = f"ondemand"
        aioschedule.every().day.at("21:25").do(self.start_db_updater, upd_msg=upd_msg)
        upd_msg = f"hourly"
        aioschedule.every().hour.at(":26").do(self.start_db_updater, upd_msg=upd_msg)
        while True:
            await aioschedule.run_pending()
            time.sleep(1)



if __name__ == '__main__':
    main_class = Main()
    loop = asyncio.new_event_loop()
    # task1 = asyncio.create_task(main_class.main_async(count=1))
    # task2 = asyncio.create_task(main_class.main_async(count=2))
    # print(asyncio.run_coroutine_threadsafe(main_class.main_async(count=1), loop=loop))
    # print(asyncio.run_coroutine_threadsafe(main_class.main_async(count=1), loop=loop))
    print(asyncio.run(main_class.main_async(count=1)))
    # main_class.main()
    # while True:
    #     now = time.ctime()
    #     # memory_system = dict(psutil.virtual_memory()._asdict())
    #     memory_used = round(psutil.virtual_memory().used/1073741824, 2)
    #     memory_msg = f"memory usage: {psutil.virtual_memory().percent}% ({memory_used})Gb"
    #     cpu_msg = f"cpu usage: {psutil.cpu_percent(interval=None)}%"
    #     msg_line = f"CAP msg from admin\n at {now}:\n {memory_msg}\n {cpu_msg}"
    #     main_class.socket_service.admin_client.send_socket_msg(to_user="telegram",
    #                                                            msg_text=msg_line)
    #     time.sleep(108000)

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
