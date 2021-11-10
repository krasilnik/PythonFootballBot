from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from tg_bot.config import TG_TOKEN
#from tg_bot.config import TG_API_URL


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat.id,
        text="Hello!!!! Send me something!",
    )


def do_echo(bot: Bot, update: Update):
    text = update.message.text
    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


def main():
    bot = Bot(
        token=TG_TOKEN,
        #base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
