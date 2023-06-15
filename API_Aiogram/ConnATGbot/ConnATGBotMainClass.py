import time
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from API_Aiogram.ATGBotMainClass import ATGBotMainClass
from API_Aiogram.ConnATGbot.ConnATGBConfig import ConnATGBConfig
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
from aiogram.types import InputFile
import nest_asyncio
from threading import Thread


class ConnATGBotMainClass(ATGBotMainClass):
    """ main class for API Telegram"""
    __token = None
    admin_id = None
    count = 0
    users_group_name_dict = dict()  # {'fin':['alex', 'mans']}
    users_group_ids_dict = dict()  # {'fin':['365758', '9595873']}
    users_id_name_dict = dict()  # {'75768996': 'alex'}
    employees_set = set()
    outgoing_dict_msgs_list = []
    incoming_msg_list = []

    def __init__(self):
        super().__init__()
        self.main_loop = None
        self.bot = None
        self.dp = None
        try:
            config = ConnATGBConfig()
            self.__token = config.get_config()['TELEGRAMBOT']['token']
            self.convert_users_2ids(config=config)
            self.admin_id = self.users_group_ids_dict.get('admin', None)[0]
            print(f"TelegramBot administrated by {self.admin_id}")

        except Exception as e:
            self.logger.warning("Cant read configuration!", e)
        else:
            # self.start_telegrambot()
            self.logger.debug(f"{__class__.__name__} runs TBot")

    def convert_users_2ids(self, config):
        groups = config.get_config()['GROUPS']
        users = config.get_config()['USERS']
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
        print(f"Serman employees: {self.employees_set}")
        return True

    def send_msg_tgbot_2admin(self, msg_text: str, from_user_id: str = None):
        msg_dict = dict({"text": msg_text})
        msg_dict["from"] = from_user_id
        msg_dict["to"] = self.admin_id
        self.outgoing_dict_msgs_list.append(msg_dict)
        return True

    def start_telegrambot(self):
        print("start async tgbot")
        first_msg = dict({"from": "tgbot", "to": self.admin_id,
                          "text": f"aiogram bot strats", "at": time.ctime()})
        self.outgoing_dict_msgs_list.append(first_msg)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.polling_bot(loop))

    async def polling_bot(self, loop):
        nest_asyncio.apply()
        bot = Bot(token=self.__token, loop=loop)
        dp = Dispatcher(bot, storage=MemoryStorage())

        @dp.message_handler(commands=['file'])
        async def request_file(message: types.Message):
            """This handler will be called when user sends `/file` command"""
            data_dict = await get_table_data()
            # print(f"data gathered")
            if type(data_dict) == dict:
                msg_dict = data_dict
                msg_dict["text"] = data_dict.get("table_name", "unknown table")
            else:
                msg_dict = dict()
                msg_dict["text"] = "cant get data from sql"
            msg_dict["to"] = message.from_user.id
            # print(f"added new msg {msg_dict['text']}")
            self.outgoing_dict_msgs_list.append(msg_dict)
            # await message.reply(f"Hi!\n gets file command {user_id}")

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
                # await send_message(user_id=self.admin_id, text=f" User {user_name} ({user_id}) send msg {msg_text} ")
                # await self.message_outcome()
                self.logger.warning(f"unknown user {user_id} send msg to chat")
            else:
                await message.answer(
                    f"Hi {user_name} ({user_id})! You are not in staff list, please send request to admin {self.admin_id}")
                await send_message(user_id=self.admin_id,
                                   text=f" Unknown user {user_name} ({user_id}) send msg {msg_text} ")
                self.logger.warning(f"unknown user {user_id} send msg to chat")

        async def send_file_2user(user_id: int, file_path, file_name):
            current_time = datetime.datetime.now().strftime('%y:%m:%d %H:%M:%S')
            print(f"sending file 2user {self.users_id_name_dict.get(str(user_id), user_id)}")
            try:
                file_send = open(file_path, "rb")
                msg_text = f"at {current_time} send file {file_name}"
                await bot.send_document(chat_id=user_id, document=file_send, caption=msg_text)
            except Exception as e:
                print(e)

        async def msg_dict_handler(msg_dict: dict):
            """ handler for dict messages translate dictionary to html text"""
            text_html = f"at:<strong>{msg_dict.get('at', time.ctime())}</strong>\n " \
                        f"from:<strong>{msg_dict.get('from', 'unknown')}</strong>\n " \
                        f"new message: <b>{msg_dict.get('text', 'empty')}</b>"
            return text_html

        async def send_message(user_id: int, text: str = None, msg_dict: dict = None, disable_notification: bool = False) -> bool:
            """
                Safe messages sender
                :param user_id:
                :param text:
                :param disable_notification:
                :return:
                """
            if msg_dict:
                text = await msg_dict_handler(msg_dict)
            try:
                await bot.send_message(user_id, text, disable_notification=disable_notification, parse_mode='HTML')
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

        async def get_table_data():
            """ gets table {"table_name": table_name, "pd_dataframe": pd_data, "file_path": excell_path}"""
            from AcyncSQL.AsyncSQLMain import AsyncSQLMain
            data = await AsyncSQLMain().async_get_pd_data_from_table_with_path('payments_in_table')
            return data

        async def sending_scheduled_msg_from_queue():
            """ gets messages from list and send them"""
            while True:
                await asyncio.sleep(5)
                while self.outgoing_dict_msgs_list:
                    self.count += 1
                    msg_dict = self.outgoing_dict_msgs_list.pop()
                    current_time = datetime.datetime.now().strftime('%y:%m:%d %H:%M:%S')
                    if type(msg_dict) == dict:
                        to_user = msg_dict.get("to", self.admin_id)
                        msg_text = msg_dict.get("text", "no text in msg")
                        print(f"gets new msg for queue {self.users_id_name_dict.get(str(to_user), to_user)}")
                        if msg_dict.get("table_name", None):
                            file_path = msg_dict.get("file_path", None)
                            file_name = msg_dict.get("table_name", None)
                            await send_file_2user(user_id=to_user, file_path=file_path, file_name=file_name)
                        else:
                            await send_message(user_id=to_user, msg_dict=msg_dict)
                            continue
                    else:
                        await send_message(user_id=self.admin_id,
                                           text=f"{current_time}\n {self.count} message: {msg_dict}")
            return True

        async def scheduled_loop():
            """ test loop for debugging put messages in outgoing list"""
            while True:
                await asyncio.sleep(3600)
                text = f"aiogram bot send report every hour"
                data_dict = dict({"from": "tgbot", "to": self.admin_id, "text": text, "at": time.ctime()})
                if type(data_dict) == dict:
                    msg_dict = data_dict
                    msg_dict["text"] = data_dict.get("text", "unreadable text")
                else:
                    msg_dict = dict()
                    msg_dict["text"] = "cant get data from sql"
                msg_dict["to"] = self.admin_id
                self.outgoing_dict_msgs_list.append(msg_dict)
        asyncio.create_task(scheduled_loop())


        asyncio.create_task(scheduled_loop())
        asyncio.create_task(sending_scheduled_msg_from_queue())
        asyncio.create_task(executor.start_polling(dp, skip_updates=True))

        # asyncio.gather(sending_scheduled_msg_from_queue(), executor.start_polling(dp, skip_updates=True))

        # polling_task = asyncio.run_coroutine_threadsafe(executor.start_polling(dp, skip_updates=True), loop=loop)
        # polling_task.result()


        return True


# def main():
#     connector = ConnTGBotMainClass()
#     loop = asyncio.new_event_loop()
#     coro = connector.start_telegrambot()
#     start_tg_task = asyncio.run_coroutine_threadsafe(coro, loop)
#     print(start_tg_task.result())


if __name__ == '__main__':
    connector = ConnTGBotMainClass()
    connector.start_telegrambot()
    # current_loop = asyncio.new_event_loop()
    Thread(target=connector.start_telegrambot, args=[]).start()
    # main()
    print("run in background")
