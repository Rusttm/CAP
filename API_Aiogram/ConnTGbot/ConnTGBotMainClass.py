from API_Aiogram.TGBotMainClass import TGBotMainClass
from API_Aiogram.ConnTGbot.ConnTGBConfig import ConnTGBConfig
from aiogram import Bot, Dispatcher, executor, types


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
        bot = Bot(token=self.__token)
        dp = Dispatcher(bot)


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
        async def echo(message: types.Message):
            # old style:
            # await bot.send_message(message.chat.id, message.text)
            await message.answer(message.text)

        executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    connector = ConnTGBotMainClass()

