import schedule
import time
import datetime
import telebot
import threading
from telebot import types
from dict_id_chats import user_dict
from info_pets import info_dog, info_cat, info_panda, food_meet, food_green, food_all
from pet import Pet
from life import feed_pet, walk_pet, wash_pet, check_heel


bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')


@bot.message_handler(commands=['start'])
def hello(message):
    tip_pitomca = types.InlineKeyboardMarkup()
    dog = types.InlineKeyboardButton('🐶', callback_data='dog')
    cat = types.InlineKeyboardButton('🐱', callback_data='cat')
    panda = types.InlineKeyboardButton('🐼', callback_data='panda')
    tip_pitomca.add(dog, cat, panda)
    bot.send_message(message.chat.id, 'Привет, давай выберем твоего питомца!', reply_markup=tip_pitomca)



@bot.callback_query_handler(func=lambda call: call.data == 'dog')
def dog(call):
    prove = types.InlineKeyboardMarkup()
    button_prove = types.InlineKeyboardButton('Подтвердить выбор', callback_data='prove_dog')
    button_exit = types.InlineKeyboardButton('Отмена', callback_data='exit')
    prove.add(button_prove, button_exit)
    bot.send_message(call.from_user.id, '🐶 Гав-Гав')
    bot.send_message(call.from_user.id, f'{info_dog}', reply_markup=prove)


@bot.callback_query_handler(func=lambda call: call.data == 'cat')
def cat(call):
    prove = types.InlineKeyboardMarkup()
    button_prove = types.InlineKeyboardButton('Подтвердить выбор', callback_data='prove_cat')
    button_exit = types.InlineKeyboardButton('Отмена', callback_data='exit')
    prove.add(button_prove, button_exit)
    bot.send_message(call.from_user.id, '🐱 Мяу Мяу')
    bot.send_message(call.from_user.id, f'{info_cat}', reply_markup=prove)


@bot.callback_query_handler(func=lambda call: call.data == 'panda')
def panda(call):
    prove = types.InlineKeyboardMarkup()
    button_prove = types.InlineKeyboardButton('Подтвердить выбор', callback_data='prove_panda')
    button_exit = types.InlineKeyboardButton('Отмена', callback_data='exit')
    prove.add(button_prove, button_exit)
    bot.send_message(call.from_user.id, '🐼 Нгяньгь')
    bot.send_message(call.from_user.id, f'{info_panda}', reply_markup=prove)



@bot.callback_query_handler(func=lambda call: call.data == 'exit')
def exit(call):
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.delete_message(call.from_user.id, call.message.message_id - 1)


@bot.callback_query_handler(func=lambda call: call.data == 'prove_dog')
def prove_dog(call):
    bot.send_message(call.from_user.id, 'Отлично теперь 🐶 ваш питомец! Придумайте ему имя и напишите его!')
    bot.register_next_step_handler(call.message, named_pet)
    global pet_tipe
    pet_tipe = '🐶'


@bot.callback_query_handler(func=lambda call: call.data == 'prove_cat')
def prove_cat(call):
    bot.send_message(call.from_user.id, 'Отлично теперь 🐱 ваш питомец! Придумайте ему имя и напишите его!')
    bot.register_next_step_handler(call.message, named_pet)
    global pet_tipe
    pet_tipe = '🐱'


@bot.callback_query_handler(func=lambda call: call.data == 'prove_panda')
def prove_panda(call):
    bot.send_message(call.from_user.id, 'Отлично теперь 🐼 ваш питомец! Придумайте ему имя и напишите его!')
    bot.register_next_step_handler(call.message, named_pet)
    global pet_tipe
    pet_tipe = '🐼'


def named_pet(message):
    pet_name = message.text
    bot.send_message(message.chat.id, f'Отлично, {pet_name} - хорошее имя для {pet_tipe}!')
    moy_pet = Pet(message.chat.id, pet_tipe, True, 10, 10, pet_name, False, False, False, time.time())
    user_dict[message.chat.id] = moy_pet
    print(user_dict)
    if len(user_dict) == 1:
        start_check()



def check():
    def check_potok(key, pet):
        if pet.life_status['life_status'] == True and pet.life_status['message'] == False:
            if pet.need_food['need_food'] == True and pet.need_food['message'] == False:
                bot.send_message(key, f'Питомец голоден!')
                pet.need_food['message'] = True
            if pet.need_walk['need_walk'] == True and pet.need_walk['message'] == False:
                bot.send_message(key, f'Питомец хочет на улицу!')
                pet.need_walk['message'] = True
            if pet.need_wash['need_wash'] == True and pet.need_wash['message'] == False:
                bot.send_message(key, f'Питомца пора помыть!')
                pet.need_wash['message'] = True
        elif pet.life_status['life_status'] == False and pet.life_status['message'] == False:
            time_diff = datetime.timedelta(seconds=time.time() - pet.time)
            days, seconds = time_diff.days, time_diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60

            message_text = f"{days} дней, {hours} часов, {minutes} минут, {seconds} секунд"
            bot.send_message(key, f'Ваш питомец погиб! Он был с вами так мало времени, но он останется в вашем сердце навсегда.\n'
                                  f'Ваш питомец был с вами:\n'
                                  f'{message_text}')
            pet.life_status['message'] = True

    for key, pet in user_dict.items():
        print(key)
        potok = threading.Thread(target=check_potok, args=(key, pet,))
        potok.start()


schedule.every(5).minutes.do(check)
schedule.every(61).minutes.do(feed_pet)
schedule.every(92).minutes.do(walk_pet)
schedule.every(119).minutes.do(wash_pet)
schedule.every().day.at('10:00').do(check_heel)


def start_check():
    while 1:
        schedule.run_pending()
        time.sleep(1)



@bot.message_handler(commands=['help'])
def info(message):
    bot.send_message(message.chat.id, f'Вот список всех команд которые доступны в этом боте: \n'
                                      f'1. /start - Начинает создание вашего питомца \n'
                                      f'2. /info - Выводит на экран информацию о вашем питомце')


@bot.message_handler(commands=['keel'])
def info(message):
    if message.chat.id not in user_dict:
        bot.send_message(message.chat.id, 'Вы пока ещё не завели питомца( \n'
                                          'Давайте это исправим, жмите /start !')
    else:
        bot.send_message(message.chat.id, f'Вы бесчеловечно убили вашего питомца. Чем же {user_dict[message.chat.id].name} заслужил(ла) такого обращения? У вас нет ничего святого. Удалите, пожалуйста, этого бота и никогда сюда не возвращайтесь')
        user_dict[message.chat.id].hp = 0
        user_dict[message.chat.id].life_status['life_status'] = False
        check()


@bot.message_handler(commands=['info'])
def info(message):
    if message.chat.id not in user_dict:
        bot.send_message(message.chat.id, 'Вы пока ещё не завели питомца( \n'
                                          'Давайте это исправим, жмите /start !')
    else:
        time_diff = datetime.timedelta(seconds=time.time() - user_dict[message.chat.id].time)
        days, seconds = time_diff.days, time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        message_text = f"{days} дней, {hours} часов, {minutes} минут, {seconds} секунд"

        bot.send_message(message.chat.id, f'Ваш питомец - {user_dict[message.chat.id].tipe}\n'
                                          f'Имя вашего питомца - {user_dict[message.chat.id].name}\n'
                                          f'Здоровье вашего питомца - {user_dict[message.chat.id].hp} из 10!\n'
                                          f'Ваш питомец с вами уже:\n'
                                          f'{message_text}')


@bot.message_handler()
def message(message):
    print(message)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'прив')
        print('есть контакт')
    if message.text.lower() == 'гуляю':
        user_dict[message.chat.id].got_walk()
        bot.send_message(message.chat.id, 'питомец погулял')
    if message.text.lower() == 'мою':
        user_dict[message.chat.id].got_wash()
        bot.send_message(message.chat.id, 'питомец помыт')

    for i in message.text:
        if i in food_all:
            if user_dict[message.chat.id].tipe == '🐶':
                if i in food_meet:
                    user_dict[message.chat.id].got_food()
                    bot.send_message(message.chat.id, f'Питомец покормлен! {user_dict[message.chat.id].name} в восторге от {i}')
                else:
                    bot.send_message(message.chat.id, f'{i} - эта еда {user_dict[message.chat.id].name} не понравилась, не давайте больше такое вашему питомцу.')

            if user_dict[message.chat.id].tipe == '🐱':
                if i in food_meet:
                    user_dict[message.chat.id].got_food()
                    bot.send_message(message.chat.id, f'Питомец покормлен! {user_dict[message.chat.id].name} в восторге от {i}')
                else:
                    bot.send_message(message.chat.id, f'{i} - эта еда {user_dict[message.chat.id].name} не понравилась, не давайте больше такое вашему питомцу.')

            if user_dict[message.chat.id].tipe == '🐼':
                if i in food_green:
                    user_dict[message.chat.id].got_food()
                    bot.send_message(message.chat.id,
                                     f'Питомец покормлен! {user_dict[message.chat.id].name} в восторге от {i}')
                else:
                    bot.send_message(message.chat.id,
                                     f'{i} - эта еда {user_dict[message.chat.id].name} не понравилась, не давайте больше такое вашему питомцу.')




bot.polling(none_stop=True)