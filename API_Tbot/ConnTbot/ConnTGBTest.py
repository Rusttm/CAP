#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

from API_Tbot.ConnTbot.ConnTGBotMainClass import ConnTGBotMainClass
from API_Tbot.ConnTbot.ConnTGBConfig import ConnTGBConfig
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class ConnTGBTest(ConnTGBotMainClass):
    __token = None
    def __init__(self):
        super().__init__()
        try:
            self.__token =ConnTGBConfig().get_config()['token']
            print(self.__token)
        except Exception as e:
            self.logger.warning("Cant read configuration!", e)



    # def start_telegrambot(self):
    #     # print(self.re)
    #     async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #         await update.message.reply_text(f'Hello {update.effective_user.first_name}')
    #
    #     app = ApplicationBuilder().token("YOUR TOKEN HERE").build()
    #
    #     app.add_handler(CommandHandler("hello", hello))
    #
    #     app.run_polling()






if __name__ == '__main__':
    connector = ConnTGBTest()
    # connector.set_config()
    # connector.start_telegrambot()