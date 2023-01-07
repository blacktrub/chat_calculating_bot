import decimal
from decimal import Decimal
import operator
from typing import List

import telebot

from constants import TOKEN

bot = telebot.TeleBot(TOKEN)

OPERATION_MAP = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.truediv,
    "*": operator.mul,
}


def is_expression(s: str) -> bool:
    s = s.strip().replace(" ", "")
    for x in (" ", *"".join(str(x) for x in range(10)), *OPERATION_MAP.keys()):
        s = s.replace(x, "")
    return s == ""


def expression_parser(s: str) -> List[str]:
    s = s.strip().replace(" ", "")
    res = []
    j = i = 0
    while i < len(s):
        if s[i] in OPERATION_MAP.keys():
            res.append(s[j:i])
            res.append(s[i])
            j = i + 1
        i += 1

    res.append(s[j:i].strip())
    return res


def calculate(operations: List[str]) -> Decimal:
    # Frist of all we perform high priority operators
    i = 0
    while i < len(operations):
        if operations[i] in ("*", "/"):
            first, second = Decimal(operations[i - 1]), Decimal(operations[i + 1])
            operations[i - 1] = OPERATION_MAP[operations[i]](first, second)
            operations.pop(i)
            operations.pop(i)
        else:
            i += 1

    # Now we can do the rest
    i = 0
    while i < len(operations):
        if not operations[i].isnumeric():
            first, second = Decimal(operations[i - 1]), Decimal(operations[i + 1])
            operations[i - 1] = OPERATION_MAP[operations[i]](first, second)
            operations.pop(i)
            operations.pop(i)
        else:
            i += 1

    return Decimal(operations[0])


@bot.message_handler()
def listen_all_messages(message):
    if not is_expression(message.text):
        return

    operations = expression_parser(message.text)
    try:
        result = calculate(operations)
    except (ZeroDivisionError, decimal.InvalidOperation):
        return

    bot.reply_to(message, f"= {result}")


bot.polling(none_stop=True)
