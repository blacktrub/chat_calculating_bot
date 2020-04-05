import telebot

from constants import TOKEN

bot = telebot.TeleBot(TOKEN)

bot.polling()
