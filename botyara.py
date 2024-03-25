import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import telebot
from dotenv import load_dotenv
import os


class SummarizationNeuralNetwork(nn.Module):
    def __init__(self):
        super(SummarizationNeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(1, 1)

    def forward(self, x):
        x = self.fc1(x)
        return x


load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))

with open('forbw.txt', 'r', encoding='utf8') as file:
    forbidden_words = [word.strip().lower().replace(', ', ' ') for word in file.readlines()]

net = SummarizationNeuralNetwork()
optimizer = optim.SGD(net.parameters(), lr=0.01, momentum=0.9)

conversation_memory = []


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет!")


@bot.message_handler(commands=['summarize'])
def ask_num_messages(message):
    bot.send_message(message.chat.id, "Сколько сообщений нужно суммаризировать?")
    bot.register_next_step_handler(message, summarize_messages)


def summarize_messages(message):
    try:
        num_messages = int(message.text)
        if num_messages <= 0:
            bot.send_message(message.chat.id, "Некорректное количество сообщений. Введите положительное число.")
            return
        preprocessed_text = ', '.join(conversation_memory[-num_messages:]).lower()
        summarized_topics = summarize_topics(net, preprocessed_text,
                                             num_messages=num_messages)
        bot.send_message(message.chat.id, f"Темы: {summarized_topics}")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректное количество сообщений. Введите положительное число.")


def summarize_topics(net, text, num_messages=None):
    topics = text.split(', ')[0:num_messages]
    return ', '.join(topics)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global conversation_memory

    conversation_memory.append(message.text)
    conversation_memory = conversation_memory[-10:]

    for word in (' '.join(forbidden_words)).split():
        if word in message.text.lower():
            bot.send_message(message.chat.id, "Эй, у нас не одобряются такие выражения!")
            return
    if 'привет' in message.text.lower():
        bot.send_message(message.chat.id, "Привет, как дела?")
    elif 'кто лучший дизайнер в мире' in message.text.lower().replace('?', ''):
        bot.send_message(message.chat.id, "Дарик, что за вопросы, она вообще лучшая)")
    elif 'дарик' in message.text.lower():
        bot.send_message(message.chat.id, "Я увидел ЕЁ имя? Дарик лучшая!!")
    elif 'a*' in message.text.lower():
        bot.send_message(message.chat.id, "ГЕНИИ, ПОБЕДИТЕЛИ, ЛУЧШИЕ!")


bot.polling()