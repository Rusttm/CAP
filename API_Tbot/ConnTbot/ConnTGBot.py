#!/usr/bin/env python
# used https://docs.python-telegram-bot.org/en/stable/telegram.message.html#telegram.Message.text
from threading import Thread
import telebot

from API_Tbot.ConnTbot.ConnTGBConfig import ConnTGBConfig
from API_Tbot.ConnTbot.ConnTGBotMainClass import ConnTGBotMainClass


class ConnTGBTest(ConnTGBotMainClass):
    __token = None
    admin_id = None
    app = None
    msg_queue = []
    users_dict = {}

    def __init__(self):
        super().__init__()
        try:
            config = ConnTGBConfig()
            self.__token = config.get_config('token')
            self.admin_id = config.get_config('my_chat_id')

            print(f"this bot administrated by {self.admin_id}")
        except Exception as e:
            self.logger.warning("Cant read configuration!", e)
        else:
            # self.start_telegrambot()
            Thread(target=self.start_telegrambot, args=[]).start()
            # self.start_telegrambot()
            self.logger.debug(f"{__class__.__name__} runs TBot thread")

    def start_telegrambot(self) -> None:
        text_messages = {
            'welcome':
                u'Please welcome {name}, your id:{id} !\n\n',

            'info':
                u'My name is TeleBot,\n',

            'wrong_chat':
                u'Hi there!\nThis bot can only be used in the Serman Ltd. group chat.\n'
                u'Join us!\n'
        }
        bot = telebot.TeleBot(self.__token)

        # @bot.message_handler(func=lambda m: True, content_types=['new_chat_participant'])
        # def on_user_joins(message):
        #     # if not is_api_group(message.chat.id):
        #     #     return
        #
        #     name = message.new_chat_participant.first_name
        #     if hasattr(message.new_chat_participant,
        #                'last_name') and message.new_chat_participant.last_name is not None:
        #         name += u" {}".format(message.new_chat_participant.last_name)
        #
        #     if hasattr(message.new_chat_participant, 'username') and message.new_chat_participant.username is not None:
        #         name += u" (@{})".format(message.new_chat_participant.username)
        #
        #     bot.reply_to(message, text_messages['welcome'].format(name=name))

        @bot.message_handler(commands=['info', 'help'])
        def on_info(message):
            bot.reply_to(message, text_messages['info'])
            return

        @bot.message_handler(commands=['start'])
        def on_start(message):
            # echo
            name = message.from_user.first_name
            user_id = message.from_user.id
            bot.send_message(chat_id=user_id,
                             text=text_messages['welcome'].format(name=name, id=user_id),
                             parse_mode="HTML")      # allows "MarkdownV2"
            return

        def listener(messages):
            for message in messages:
                self.logger.info(f"{__name__} receive message: {message.text} from {message.from_user.first_name}")
                print(str(message))

        bot.set_update_listener(listener)
        bot.infinity_polling()


if __name__ == '__main__':
    ConnTGBTest()
    print("bit is working")

