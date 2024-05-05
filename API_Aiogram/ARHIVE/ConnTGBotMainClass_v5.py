
import time
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from API_Aiogram.ATGBotMainClass import TGBotMainClass
from API_Aiogram.ConnATGbot.ConnATGBConfig import ConnTGBConfig
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
import nest_asyncio
from threading import Thread

class ConnTGBotMainClass(TGBotMainClass):
    """ main class for API Telegram"""
    __token = None
    admin_id = None
    count = 0
    users_group_name_dict = dict()  # {'fin':['alex', 'mans']}
    users_group_ids_dict = dict()  # {'fin':['365758', '9595873']}
    users_id_name_dict = dict()  # {'75768996': 'alex'}
    employees_set = set()
    outgoing_msgs_list = ['initiation telegram bot aiogram successfully run']
    incoming_msg_list = []

    def __init__(self):
        super().__init__()
        self.main_loop = None
        self.bot = None
        self.dp = None
        try:
            config = ConnTGBConfig()
            self.__token = config.load_config()['TELEGRAMBOT']['token']
            self.convert_users_2ids(config=config)
            self.admin_id = self.users_group_ids_dict.get('admin', None)[0]
            print(f"TelegramBot administrated by {self.admin_id}")

        except Exception as e:
            self.logger.warning("Cant read configuration!", e)
        else:
            # self.start_telegrambot()
            self.logger.debug(f"{__class__.__name__} runs TBot")

    def convert_users_2ids(self, config):
        groups = config.load_config()['GROUPS']
        users = config.load_config()['USERS']
        for group in groups:
            temp_list_name = []
            temp_list_id = []
            for name in groups.get(group).split(','):
                user_id = users.get(name)
                self.users_id_name_dict[user_id] = name
                if name and user_id:
                    temp_list_name.append(name)
                    temp_list_id.append(user_id)
                    self.employees_set.add(user_id)
            self.users_group_name_dict[group] = temp_list_name
            self.users_group_ids_dict[group] = temp_list_id
        return True

    def send_msg_tgbot_2admin(self, msg_text: str):
        self.outgoing_msgs_list.append(msg_text)
        return True
    def start_telegrambot(self):
        print("start tegbot")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # loop = asyncio.get_event_loop()
        # self.bot = Bot(token=self.__token, loop=loop)
        # self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        # coro = self.polling_bot()
        # send_task = asyncio.run_coroutine_threadsafe(coro, loop)
        # print(send_task.result())
        asyncio.run(self.polling_bot(loop))
        # self.polling_bot(loop)
        # Thread(target=self.polling_bot, args=[loop]).start()

    async def polling_bot(self, loop):
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        nest_asyncio.apply()
        bot = Bot(token=self.__token, loop=loop)
        dp = Dispatcher(bot, storage=MemoryStorage())
        @dp.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            """
            This handler will be called when user sends `/start` or `/help` command
            """
            await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

        @dp.message_handler(regexp='(^cat[s]?$|puss)')
        async def cats(message: types.Message):
            with open('../data/cats.jpeg', 'rb') as photo:
                '''
                # Old fashioned way:
                await bot.send_photo(
                    message.chat.id,
                    photo,
                    caption='Cats are here 😺',
                    reply_to_message_id=message.message_id,
                )
                '''
                await message.reply_photo(photo, caption='Cats are here 😺')

        @dp.message_handler()
        async def listener(message: types.Message):
            """ check only employees"""
            user_name = message["from"]["first_name"]
            user_id = message["from"]["id"]
            msg_text = message.text
            self.incoming_msg_list.append(dict({"from": user_name, "id": user_id, "text": msg_text}))
            self.logger.info(f"aiogram receives message: {msg_text} from {user_name}")
            if str(user_id) in self.employees_set:
                await message.answer(f"Hi {user_name} ({user_id})! Welcome to Serman telegram service")
                await send_message(user_id=self.admin_id, text=f" User {user_name} ({user_id}) send msg {msg_text} ")
                # await self.message_outcome()
                self.logger.warning(f"unknown user {user_id} send msg to chat")
            else:
                await message.answer(f"Hi {user_name} ({user_id})! You are not in staff list, please send request to admin {self.admin_id}")
                await send_message(user_id=self.admin_id, text=f" Unknown user {user_name} ({user_id}) send msg {msg_text} ")
                self.logger.warning(f"unknown user {user_id} send msg to chat")

        async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
            """
                Safe messages sender
                :param user_id:
                :param text:
                :param disable_notification:
                :return:
                """
            try:
                await bot.send_message(user_id, text, disable_notification=disable_notification)
                # await bot.send_message(731370983, text, disable_notification=disable_notification)
            except exceptions.BotBlocked:
                self.logger.error(f"Target [ID:{user_id}]: blocked by user")
            except exceptions.ChatNotFound:
                self.logger.error(f"Target [ID:{user_id}]: invalid user ID")
            except exceptions.RetryAfter as e:
                self.logger.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
                await asyncio.sleep(e.timeout)
                return await send_message(user_id, text)  # Recursive call
            except exceptions.UserDeactivated:
                self.logger.error(f"Target [ID:{user_id}]: user is deactivated")
            except exceptions.TelegramAPIError:
                self.logger.exception(f"Target [ID:{user_id}]: failed")
            else:
                self.logger.info(f"Target [ID:{user_id}]: success")
                return True
            return False

        async def scheduled_msg():
            while True:
                self.count += 1
                await asyncio.sleep(5)
                current_time = datetime.datetime.now().strftime('%y:%m:%d :%H:%M:%S')
                while self.outgoing_msgs_list:
                    msg = self.outgoing_msgs_list.pop()
                    current_time = datetime.datetime.now().strftime('%y:%m:%d :%H:%M:%S')
                    await send_message(self.admin_id, text=f"{current_time}\n {self.count} message: {msg}")
                # await send_message(self.admin_id, text=f"{current_time}\n {self.count} message: Hi from aiogram")
            return True

        def message_outcome(loop):
            self.count = 0
            # current_loop = asyncio.get_event_loop()
            while True:
                time.sleep(3)
                self.count += 1
                coro = scheduled_msg()
                send_task = asyncio.run_coroutine_threadsafe(coro, loop)
                send_task.result()
                # asyncio.run(coro)

        # current_loop = asyncio.get_event_loop()
        # Thread(target=message_outcome, args=[current_loop]).start()

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # executor.start_polling(dp, skip_updates=True)
        # loop = asyncio.new_event_loop()
        asyncio.create_task(scheduled_msg())
        polling_task = asyncio.run_coroutine_threadsafe(executor.start_polling(dp, skip_updates=True), loop=loop)
        polling_task.result()
        return True

def main():
    connector = ConnTGBotMainClass()
    loop = asyncio.new_event_loop()
    coro = connector.start_telegrambot()
    start_tg_task = asyncio.run_coroutine_threadsafe(coro, loop)
    print(start_tg_task.result())


if __name__ == '__main__':
    connector = ConnTGBotMainClass()
    connector.start_telegrambot()
    # current_loop = asyncio.new_event_loop()
    # Thread(target=main, args=[]).start()
    # main()
    print("run in background")
