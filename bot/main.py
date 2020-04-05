import decimal
import operator

import telebot

from constants import TOKEN

bot = telebot.TeleBot(TOKEN)

OPERATION_MAP = {
    'плюс': operator.add,
    '+': operator.add,
    'минус': operator.sub,
    '-': operator.sub,
    'разделить': operator.truediv,
    '/': operator.truediv,
    'умножить': operator.mul,
    '*': operator.mul,
}


@bot.message_handler()
def listen_all_messages(message):
    # bot can work with messages from 3 part
    if len(str(message.text).split()) != 3:
        return

    one, two, three = (x.strip() for x in str(message.text).split())
    if two not in OPERATION_MAP:
        return

    try:
        one, three = float(one), float(three)
    except ValueError:
        return

    result = decimal.Decimal(OPERATION_MAP[two](one, three)).quantize(decimal.Decimal('.01'), decimal.ROUND_05UP)
    bot.reply_to(message, f'= {result}')


bot.polling(none_stop=True)
