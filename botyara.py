import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import telebot
from dotenv import load_dotenv
import os


class SimpleNeuralNetwork(nn.Module):
    def __init__(self):
        super(SimpleNeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(1, 1)

    def forward(self, x):
        x = self.fc1(x)
        return x


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

with open('forbw.txt', 'r', encoding='utf8') as file:
    forbidden_words = [word.strip().lower().replace(', ', ' ') for word in file.readlines()]

net = SimpleNeuralNetwork()
optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)

conversation_memory = []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, созданный на python.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global conversation_memory

    conversation_memory.append(message.text)

    for word in (' '.join(forbidden_words)).split():
        if word in message.text.lower():
            bot.send_message(message.chat.id, "Эй, у нас не одобряются такие выражения!")
            return
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, "Привет, как дела?")
    elif message.text.lower().replace('?', '') == 'кто лучший дизайнер в мире':
        bot.send_message(message.chat.id, "Дарик, что за вопросы, она вообще лучшая)")
    elif 'дарик' in message.text.lower():
        bot.send_message(message.chat.id, "Я увидел ЕЁ имя? Дарик лучшая!!")
    else:
        bot.send_message(message.chat.id, "Я не понимаю, что ты имеешь в виду.")


bot.polling()