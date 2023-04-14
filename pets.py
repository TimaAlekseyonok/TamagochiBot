import telebot
from telebot import types
from chat_id import ChatIDSingleton
import prove_pet


bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')
id_chata = None


info_dog = 'Тут будет информация о питомце 🐶, а также советы по уходу за ним'
info_cat = 'Тут будет информация о питомце 🐱, а также советы по уходу за ним'
info_panda = 'Тут будет информация о питомце 🐼, а также советы по уходу за ним'


def id_pet():
    global id_chata
    id_chata = ChatIDSingleton()


@bot.callback_query_handler(func=lambda call: call.data == 'dog')
def dog(call):
    prove = types.InlineKeyboardMarkup()
    button_prove = types.InlineKeyboardButton('Подтвердить выбор питомца', callback_data='prove_dog')
    button_exit = types.InlineKeyboardButton('Отмена', callback_data='exit')
    prove.add(button_prove, button_exit)
    bot.send_message(id_chata.chat_id, '🐶 Гав-Гав')
    bot.send_message(id_chata.chat_id, f'{info_dog}', reply_markup=prove)


@bot.callback_query_handler(func=lambda call: call.data == 'cat')
def cat(call):
    prove = types.InlineKeyboardMarkup()
    button_prove = types.InlineKeyboardButton('Подтвердить выбор питомца', callback_data='prove_cat')
    button_exit = types.InlineKeyboardButton('Отмена', callback_data='exit')
    prove.add(button_prove, button_exit)
    bot.send_message(id_chata.chat_id, '🐱 Мяу Мяу')
    bot.send_message(id_chata.chat_id, f'{info_cat}', reply_markup=prove)


@bot.callback_query_handler(func=lambda call: call.data == 'panda')
def panda(call):
    prove = types.InlineKeyboardMarkup()
    button_prove = types.InlineKeyboardButton('Подтвердить выбор питомца', callback_data='prove_panda')
    button_exit = types.InlineKeyboardButton('Отмена', callback_data='exit')
    prove.add(button_prove, button_exit)
    bot.send_message(id_chata.chat_id, '🐼 Нгяньгь')
    bot.send_message(id_chata.chat_id, f'{info_panda}', reply_markup=prove)


@bot.callback_query_handler(func=lambda call: call.data == 'exit')
def exit(callback):
    bot.delete_message(id_chata.chat_id, callback.message.message_id)
    bot.delete_message(id_chata.chat_id, callback.message.message_id - 1)


def callback_inline(call):
    if call.message:
        if call.data == 'prove_dog':
            prove_pet.prove_dog(call)
        elif call.data == 'prove_cat':
            prove_pet.prove_cat(call)
        elif call.data == 'prove_panda':
            prove_pet.prove_panda(call)