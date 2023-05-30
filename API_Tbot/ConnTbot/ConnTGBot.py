#!/usr/bin/env python
# used https://docs.python-telegram-bot.org/en/stable/telegram.message.html#telegram.Message.text
import time
from threading import Thread
import telebot

from API_Tbot.ConnTbot.ConnTGBConfig import ConnTGBConfig
from API_Tbot.ConnTbot.ConnTGBotMainClass import ConnTGBotMainClass


class ConnTGBot(ConnTGBotMainClass):
    """ main class for API Telegram"""
    __token = None
    admin_id = None
    users_group_name_dict = dict() # {'fin':['alex', 'mans']}
    users_group_ids_dict = dict()   # {'fin':['365758', '9595873']}
    users_id_name_dict = dict() # {'75768996': 'alex'}
    employees_set = set()
    outgoing_msgs_list = []
    incoming_msg_list = []
    # srv_msg_queue = []
    # """messages from socket server"""

    def __init__(self):
        super().__init__()
        self.bot = None
        try:
            config = ConnTGBConfig()
            self.__token = config.get_config()['TELEGRAMBOT']['token']
            self.convert_users_2ids(config=config)
            self.admin_id = self.users_group_ids_dict.get('admin', None)
            print(f"TelegramBot administrated by {self.admin_id}")
        except Exception as e:
            self.logger.warning("Cant read configuration!", e)
        else:
            # self.start_telegrambot()
            Thread(target=self.start_telegrambot, args=[]).start()
            # self.start_telegrambot()
            self.logger.debug(f"{__class__.__name__} runs TBot thread")

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

    def start_telegrambot(self) -> None:
        text_messages = {
            'welcome':
                u'Hi, {name}, your id:{id} !\n\n',

            'info':
                u'My name is TeleBot,\n',

            'reject':
                u'Hi {name} your id:{id}!\nThis bot can only be used for Serman Ltd. employees.\n'
                u'Please request permission to administrator {admin} \n'
        }
        self.bot = telebot.TeleBot(self.__token)
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

        @self.bot.message_handler(commands=['info', 'help'])
        def on_info(message):
            self.bot.reply_to(message, text_messages['info'])
            return

        @self.bot.message_handler(commands=['start'])
        def on_start(message):
            # echo
            name = message.from_user.first_name
            user_id = message.from_user.id
            self.bot.send_message(chat_id=user_id,
                             text=text_messages['welcome'].format(name=name, id=user_id),
                             parse_mode="HTML")      # allows "MarkdownV2" or "HTML"
            return

        def listener(messages):
            """ check only employees"""
            for message in messages:
                user_name = message.from_user.first_name
                user_id = message.from_user.id
                msg_text = message.text
                self.incoming_msg_list.append(dict({"from": user_name, "id": user_id, "text": msg_text}))
                self.logger.info(f"{__name__} receive message: {msg_text} from {user_name}")
                if str(user_id) in self.employees_set:
                    self.bot.reply_to(message, text_messages['welcome'].format(name=user_name, id=user_id))
                else:
                    self.bot.reply_to(message,
                                      text_messages['reject'].format(name=user_name, id=user_id, admin=self.admin_id))
                    self.logger.warning(f"unknown user {user_id} send msg to chat")

        self.bot.set_update_listener(listener)
        self.bot.infinity_polling()
        self.logger.debug(f"TelegramBot is polling")


if __name__ == '__main__':
    connector = ConnTGBot()
    print("bot is working ...")
    # connector.bot.send_message(connector.admin_id, text="hello from MainClass")



