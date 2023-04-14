import telebot
from telebot import types
from chat_id import ChatIDSingleton
import pets
import prove_pet
import life


bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')


id_chata = None


@bot.message_handler(commands=['start'])
def hello(message):
    global id_chata
    id_chata = ChatIDSingleton()
    id_chata.set_chat_id(message.chat.id)

    tip_pitomca = types.InlineKeyboardMarkup()
    dog = types.InlineKeyboardButton('🐶', callback_data='dog')
    cat = types.InlineKeyboardButton('🐱', callback_data='cat')
    panda = types.InlineKeyboardButton('🐼', callback_data='panda')
    tip_pitomca.add(dog, cat, panda)
    bot.send_message(id_chata.chat_id, 'Привет, давай выберем твоего питомца!', reply_markup=tip_pitomca)

    pets.id_pet()
    prove_pet.id_prove()
    life.id_life()


@bot.message_handler(commands=['help'])
def info(message):
    bot.send_message(id_chata.chat_id, f'Вот список всех команд которые доступны в этом боте: \n'
                                      f'1. ... \n'
                                      f'2. ... \n'
                                      f'3. ...')


@bot.message_handler(commands=['name'])
def info(message):
    if prove_pet.pitomec_name is None:
        bot.send_message(message.chat.id, 'Вы пока ещё не завели питомца( \n'
                                          'Давайте это исправим, жмите /start !')
    else:
        bot.send_message(message.chat.id, f'Ваш питомец - {prove_pet.pitomec_name}')

@bot.message_handler(commands=['health'])
def info(message):
    if life.pet_health is None:
        bot.send_message(message.chat.id, 'Вы пока ещё не завели питомца( \n'
                                          'Давайте это исправим, жмите /start !')
    else:
        bot.send_message(message.chat.id, f'Здоровье вашего питомца - {life.pet_health.health} из 10!')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:

        if call.data == 'dog':
            pets.dog(call)
        elif call.data == 'cat':
            pets.cat(call)
        elif call.data == 'panda':
            pets.panda(call)
        elif call.data == 'exit':
            pets.exit(call)

        else:
            pets.callback_inline(call)


@bot.message_handler(func=lambda message: prove_pet.pet_chosen == True)
def message(message):
    prove_pet.message(message)


@bot.message_handler()
def message(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'прив')
    elif message.text == '🍗':
        life.need_food = False
    elif message.text == 'гуляю':
        life.need_walk = False
    elif message.text == 'мою':
        life.need_wash = False




bot.polling(none_stop=True)