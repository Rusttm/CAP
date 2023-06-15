import time

from API_Aiogram.ContATGbot.ContATGBotMainClass import ContATGBotMainClass
from API_Aiogram.ConnATGbot.ConnATGBotMainClass import ConnATGBotMainClass


class ContATGBot(ContATGBotMainClass, ConnATGBotMainClass):
    """ Controller for aiogram api """

    def __init__(self):
        super().__init__()

    def send_service_msg(self, msg=None):
        """ send msg to telegrambot user in admin group"""
        for admin in self.users_group_ids_dict.get('admin', []):
            try:
                text_html = f"at:<strong>{msg.get('at', time.ctime())}</strong>\n " \
                            f"from:<strong>{msg.get('from','unknown')}</strong>\n " \
                            f"new message: <b>{msg.get('text', 'empty')}</b>"
                msg = text_html
            except Exception as e:
                self.logger.warning(f" tgbot cant format dict {msg} to text ")
        self.send_msg_tgbot_2admin(msg_text=f"msg from service {msg}")
            # self.bot.send_message(chat_id=admin, text=msg, parse_mode="HTML")  # allowed "MarkdownV2"

    def send_finance_msg(self, msg=None):
        """ send msg to telegrambot user in fin group"""
        for fin in self.users_group_ids_dict.get('fin', []):
            self.send_msg_tgbot_2admin(msg_text=f"msg from service {msg}")
            # self.bot.send_message(chat_id=fin, text=msg, parse_mode="HTML")

    def send_spam_msg(self, msg=None):
        """ send msg to telegrambot user in all groups"""
        for _, group_list in self.users_group_ids_dict.items():
            for user_id in group_list:
                self.bot.send_message(chat_id=user_id, text=msg, parse_mode="HTML")
                try:
                    name = self.users_id_name_dict[user_id]
                    self.outgoing_msgs_list.append(dict({"to": name, "id": user_id, "msg": msg, "at": f"{time.ctime()}"}))
                except Exception as e:
                    self.logger.warning(f"{__file__.__name__} cant find name for id: {user_id}")

    def get_incoming_msg_list(self):
        msg_list = self.incoming_msg_list
        self.incoming_msg_list = []
        return msg_list

    def get_outgoing_msg_list(self):
        msg_list = self.outgoing_dict_msgs_list
        self.outgoing_msgs_list = []
        return msg_list


if __name__ == '__main__':
    connector = ContATGBot()
    print("bot is working ...")
    # connector.send_spam_msg(msg=f"Hello iam spam")
    time.sleep(10)
    print(connector.get_incoming_msg_list())
    print(connector.get_outgoing_msg_list())
    # for i in range(4):
    #     connector.send_finance_msg(msg=f"{i}Hello my friend")
    #     time.sleep(3)
