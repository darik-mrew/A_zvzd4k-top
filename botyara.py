import telebot

bot = telebot.TeleBot('7158913332:AAGTwi6hz3QDoCxoDHyVzKMmxnTbcjQczUA')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, созданный на Python.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет, как дела?")
    else:
        bot.send_message(message.chat.id, "Я не понимаю, что ты имеешь в виду.")
bot.polling()