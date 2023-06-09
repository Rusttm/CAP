from API_Aiogram.TGBotMainClass import TGBotMainClass
from API_Aiogram.ConnTGbot.ConnTGBConfig import ConnTGBConfig
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
import nest_asyncio
from threading import Thread

class ConnTGBotMainClass(TGBotMainClass):
    """ main class for API Telegram"""
    __token = None
    admin_id = None
    users_group_name_dict = dict()  # {'fin':['alex', 'mans']}
    users_group_ids_dict = dict()  # {'fin':['365758', '9595873']}
    users_id_name_dict = dict()  # {'75768996': 'alex'}
    employees_set = set()
    outgoing_msgs_list = []
    incoming_msg_list = []

    def __init__(self):
        super().__init__()
        self.bot = None
        self.dp = None
        try:
            config = ConnTGBConfig()
            self.__token = config.get_config()['TELEGRAMBOT']['token']
            self.convert_users_2ids(config=config)
            self.admin_id = self.users_group_ids_dict.get('admin', None)
            print(f"TelegramBot administrated by {self.admin_id}")

        except Exception as e:
            self.logger.warning("Cant read configuration!", e)
        else:
            self.start_telegrambot()
            # Thread(target=self.start_telegrambot, args=[]).start()
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
        return True

    def start_telegrambot(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(self.polling_bot())
        loop.run_until_complete(task)

    async def polling_bot(self):
        nest_asyncio.apply()
        self.bot = Bot(token=self.__token)
        dp = Dispatcher(self.bot)

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

        # @dp.message_handler()
        # async def echo(message: types.Message):
        #     # old style:
        #     # await bot.send_message(message.chat.id, message.text)
        #     print(message.text)
        #     print(message)
        #     await message.answer(message.text)
        # the on_throttled object can be either a regular function or coroutine

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
                await self.bot.send_message(user_id, text, disable_notification=disable_notification)
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
        async def message_outcome():
            while True:
                await asyncio.sleep(2)
                print("test time")
            return True
        executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    connector = ConnTGBotMainClass()
