import schedule
import time
import datetime
import telebot
from telebot import types
from info_pets import info_dog, info_cat, info_panda, food_meet, food_green, food_all, illness_heel
from class_bd import create_connection_factory, get_connection
from life import feed_pet, walk_pet, wash_pet, check_heel, illness_pet



bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')
create_connection_factory('D:/00-IT-00/TelegramBot/mydatabase.db')


@bot.message_handler(commands=['on'])
def on(message):
    bot.send_message(message.chat.id, 'Пошло!')
    check_database()



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

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT OR IGNORE INTO users (id) VALUES ({message.chat.id})")
    cursor.execute(f"UPDATE users SET (tipe, life_status, life_status_message, last_hp, hp, name, need_food, need_food_message, need_walk, need_walk_message, need_wash, need_wash_message, time, illness, illness_message) = "
                   f"('{pet_tipe}', True, False, 10, 10, '{pet_name}', False, False, False, False, False, False, {time.time()}, False, False) WHERE id = {message.chat.id}")
    conn.commit()

    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    # Выводим полученные записи
    for row in rows:
        print(row)




def check():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE life_status == True AND '
                   'life_status_message == False AND '
                   'need_food == True AND '
                   'need_food_message == False')
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            bot.send_message(id, 'Питомец голоден!')
            cursor.execute(f"UPDATE users SET need_food_message = True WHERE id = {id}")
            conn.commit()


    cursor.execute('SELECT * FROM users WHERE life_status == True AND '
                   'life_status_message == False AND '
                   'need_walk == True AND '
                   'need_walk_message == False')
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            bot.send_message(id, 'Питомец хочет на улицу!')
            cursor.execute(f"UPDATE users SET need_walk_message = True WHERE id = {id}")
            conn.commit()


    cursor.execute('SELECT * FROM users WHERE life_status == True AND '
                   'life_status_message == False AND '
                   'need_wash == True AND '
                   'need_wash_message == False')
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            bot.send_message(id, 'Питомца пора помыть!')
            cursor.execute(f"UPDATE users SET need_wash_message = True WHERE id = {id}")
            conn.commit()

    cursor.execute('SELECT * FROM users WHERE life_status == True AND '
                   'life_status_message == False AND '
                   'illness == True AND '
                   'illness_message == False')
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            bot.send_message(id, 'Питомец заболел!')
            cursor.execute(f"UPDATE users SET illness_message = True WHERE id = {id}")
            conn.commit()


    cursor.execute('SELECT * FROM users WHERE life_status == False AND '
                   'life_status_message == False')
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            time = row[13]
            time_diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(time)
            days, seconds = time_diff.days, time_diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            message_text = f"{days} дней, {hours} часов, {minutes} минут, {seconds} секунд"
            bot.send_message(id, f'Ваш питомец погиб! Он был с вами так мало времени, но он останется в вашем сердце навсегда.\n'
                             f'Ваш питомец был с вами:\n'
                             f'{message_text}')
            cursor.execute(f"UPDATE users SET life_status_message = True WHERE id = {id}")
            conn.commit()



schedule.every(5).minutes.do(check)
schedule.every(61).minutes.do(feed_pet)
schedule.every(92).minutes.do(walk_pet)
schedule.every(123).minutes.do(wash_pet)
schedule.every(3).hours.do(check_heel)
schedule.every(3).hours.do(illness_pet)
# schedule.every().day.at('10:00').do(check_heel)


def start_check():
    while 1:
        schedule.run_pending()
        time.sleep(1)


def check_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM users")
    result = cursor.fetchone()[0]
    if result > 0:
        start_check()
    conn.close()



@bot.message_handler(commands=['help'])
def info(message):
    bot.send_message(message.chat.id, f'Вот список всех команд которые доступны в этом боте: \n'
                                      f'1. /start - Начинает создание вашего питомца \n'
                                      f'2. /info - Выводит на экран информацию о вашем питомце')


@bot.message_handler(commands=['kill'])
def kill(message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id == {message.chat.id} AND "
                   "life_status_message == False")
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            name = row[6]
            bot.send_message(id, f'Вы бесчеловечно убили вашего питомца. Чем же {name} заслужил(ла) такого обращения? У вас нет ничего святого. Удалите, пожалуйста, этого бота и никогда сюда не возвращайтесь')
            cursor.execute(f"UPDATE users SET (hp, life_status, life_status_message) = (0, False, True) WHERE id = {id}")
            conn.commit()
    else:
        bot.send_message(message.chat.id, 'Вы пока ещё не завели питомца( \n'
                                          'Давайте это исправим, жмите /start !')


@bot.message_handler(commands=['info'])
def info(message):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id == {message.chat.id}")
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            tipe = row[1]
            hp = row[5]
            name = row[6]
            time = row[13]
            time_diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(time)
            days, seconds = time_diff.days, time_diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            message_text = f"{days} дней, {hours} часов, {minutes} минут, {seconds} секунд"
            bot.send_message(id, f'Ваш питомец - {tipe}\n'
                                                      f'Имя вашего питомца - {name}\n'
                                                      f'Здоровье вашего питомца - {hp} из 10!\n'
                                                      f'Ваш питомец с вами уже:\n'
                                                      f'{message_text}')
            conn.commit()
    else:
        bot.send_message(message.chat.id, 'Вы пока ещё не завели питомца( \n'
                                          'Давайте это исправим, жмите /start !')



@bot.message_handler()
def message(message):
    print(message)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'прив')

    if message.text.lower() == 'гуляю':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id == {message.chat.id}")
        result = cursor.fetchall()
        if result:
            for row in result:
                id = row[0]
                bot.send_message(id, 'Питомец погулял')
                cursor.execute(f"UPDATE users SET (need_walk, need_walk_message) = (False, False) WHERE id = {id}")
                conn.commit()

    if message.text.lower() == 'мою':
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id == {message.chat.id}")
        result = cursor.fetchall()
        if result:
            for row in result:
                id = row[0]
                bot.send_message(message.chat.id, 'Питомец помыт')
                cursor.execute(f"UPDATE users SET (need_wash, need_wash_message) = (False, False) WHERE id = {id}")
                conn.commit()

    for i in message.text:
        if i in illness_heel:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE id == {message.chat.id}")
            result = cursor.fetchall()
            if result:
                for row in result:
                    id = row[0]
                    bot.send_message(message.chat.id, 'Питомец здоров!')
                    cursor.execute(f"UPDATE users SET (illness, illness_message) = (False, False) WHERE id = {id}")
                    conn.commit()

    for i in message.text:
        if i in food_all:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users WHERE id == {message.chat.id}")
            result = cursor.fetchall()
            if result:
                for row in result:
                    id = row[0]
                    tipe = row[1]
                    name = row[6]
                    if tipe == '🐶':
                        if i in food_meet:
                            cursor.execute(f"UPDATE users SET (need_food, need_food_message) = (False, False) WHERE id = {id}")
                            conn.commit()
                            bot.send_message(message.chat.id, f'Питомец покормлен! {name} в восторге от {i}')
                        else:
                            bot.send_message(message.chat.id, f'{i} - эта еда {name} не понравилась, не давайте больше такое вашему питомцу.')

                    if tipe == '🐱':
                        if i in food_meet:
                            cursor.execute(f"UPDATE users SET (need_food, need_food_message) = (False, False) WHERE id = {id}")
                            conn.commit()
                            bot.send_message(message.chat.id, f'Питомец покормлен! {name} в восторге от {i}')
                        else:
                            bot.send_message(message.chat.id,
                                             f'{i} - эта еда {name} не понравилась, не давайте больше такое вашему питомцу.')

                    if tipe == '🐼':
                        if i in food_green:
                            cursor.execute(f"UPDATE users SET (need_food, need_food_message) = (False, False) WHERE id = {id}")
                            conn.commit()
                            bot.send_message(message.chat.id, f'Питомец покормлен! {name} в восторге от {i}')
                        else:
                            bot.send_message(message.chat.id,
                                             f'{i} - эта еда {name} не понравилась, не давайте больше такое вашему питомцу.')



bot.polling(none_stop=True)