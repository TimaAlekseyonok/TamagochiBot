import telebot
from telebot import types
from chat_id import ChatIDSingleton
import life



bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')
id_chata = None


pitomec = None
pitomec_name = None
pet_chosen = False


def id_prove():
    global id_chata
    id_chata = ChatIDSingleton()


@bot.callback_query_handler(func=lambda call: call.data == 'prove_dog')
def prove_dog(call):
    global pitomec
    pitomec = '🐶'
    bot.send_message(id_chata.chat_id, 'Отлично теперь 🐶 ваш питомец! Придумайте ему имя и напишите его!')
    global pet_chosen
    pet_chosen = True

@bot.callback_query_handler(func=lambda call: call.data == 'prove_cat')
def prove_cat(call):
    global pitomec
    pitomec = '🐱'
    bot.send_message(id_chata.chat_id, 'Отлично теперь 🐱 ваш питомец! Придумайте ему имя и напишите его!')
    global pet_chosen
    pet_chosen = True

@bot.callback_query_handler(func=lambda call: call.data == 'prove_panda')
def prove_panda(call):
    global pitomec
    pitomec = '🐼'
    global pet_chosen
    pet_chosen = True
    bot.send_message(id_chata.chat_id, 'Отлично теперь 🐼 ваш питомец! Придумайте ему имя и напишите его!')


def message(message):
    global pitomec_name
    pitomec_name = message.text
    bot.send_message(id_chata.chat_id, f'Отлично, {pitomec_name} - хорошее имя для {pitomec}!')
    global pet_chosen
    pet_chosen = False
    life.start_life = True
    life.start_life_funktion()
