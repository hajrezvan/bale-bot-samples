"""Purchase message simple conversion with bot
"""
import asyncio

from balebot.filters import *
from balebot.handlers import MessageHandler
from balebot.models.messages import *
from balebot.models.messages.banking.money_request_type import MoneyRequestType
from balebot.updater import Updater

# A token you give from BotFather when you create your bot set below
updater = Updater(token="114d273b48f04cd7c3be657328d2aa5521dae020",
                  loop=asyncio.get_event_loop())
bot = updater.bot
dispatcher = updater.dispatcher


def success(result, user_data):
    print("success : ", result)
    print(user_data)


def failure(result, user_data):
    print("failure : ", result)
    print(user_data)


@dispatcher.command_handler(["talk"])
def conversation_starter(bot, update):
    message = TextMessage("Hi , nice to meet you :)\nplease send me a photo")
    user_peer = update.get_effective_user()
    bot.send_message(message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.register_conversation_next_step_handler(update, MessageHandler(PhotoFilter(), purchase_message))


@dispatcher.message_handler(PhotoFilter())
def purchase_message(bot, update):
    message = update.get_effective_message()
    user_peer = update.get_effective_user()
    first_purchase_message = PurchaseMessage(msg=message, account_number=6037991822619544, amount=11100,
                                             money_request_type=MoneyRequestType.normal)
    bot.send_message(first_purchase_message, user_peer, success_callback=success, failure_callback=failure)
    dispatcher.finish_conversation()


updater.run()
