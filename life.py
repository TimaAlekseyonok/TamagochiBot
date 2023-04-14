import schedule
import time
import threading

import telebot
from telebot import types
from chat_id import ChatIDSingleton
from health import Health


bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')
id_chata = None


pet_health = None
last_health = 10
start_life = False
need_food = False
need_walk = False
need_wash = False

last_time_food = None
last_time_walk = None
last_time_wash = None


def id_life():
    global id_chata
    id_chata = ChatIDSingleton()



def get_damage():
    global pet_health
    pet_health.damage()
    if pet_health.health > 0:
        bot.send_message(id_chata.chat_id, f'Здоровье вашего питомца уменьшилось на 1, теперь его показатель здоровья составляет {pet_health.health} из 10!')
    else:
        bot.send_message(id_chata.chat_id, 'Ваш питомец погиб! Он был с вами так мало времени, но он останется в вашем сердце навсегда.')
        global start_life
        start_life = False

def check_heel():
    global last_health, pet_health
    if pet_health.health < 10:
        if last_health > pet_health.health:
            last_health = pet_health.health
        elif last_health == pet_health.health:
            pet_health.heel()
            last_health = pet_health.health
            bot.send_message(id_chata.chat_id, '+1')



def check_food():
    global need_food
    if need_food is False:
        bot.send_message(id_chata.chat_id, "Спасибо, что покормили питомца!")
    else:
        bot.send_message(id_chata.chat_id, "Вы не успели покормить питомца, он теряет 1 здоровье :(")
        need_food = False
        get_damage()

def whaiting_food():
    global last_time_food
    while time.time() - last_time_food < 30*60 and need_food is True:
        time.sleep(1)
    else:
        check_food()

def create_potok_food(whaiting_food_func):
    potok_food = threading.Thread(target=whaiting_food_func)
    potok_food.start()

def feed_pet():
    global need_food
    bot.send_message(id_chata.chat_id, "Ваш питомец проголодался. Его нужно покормить.")
    need_food = True
    global last_time_food
    last_time_food = time.time()
    create_potok_food(whaiting_food)



def check_walk():
    global need_walk
    if need_walk is False:
        bot.send_message(id_chata.chat_id, "Ура питомец погулял!")
    else:
        bot.send_message(id_chata.chat_id, "Вы не погуляли с малышом :(")
        need_walk = False
        get_damage()

def whaiting_walk():
    global last_time_walk
    while time.time() - last_time_walk < 30*60 and need_walk is True:
        time.sleep(1)
    else:
        check_walk()

def create_potok_walk(whaiting_walk_func):
    potok_walk = threading.Thread(target=whaiting_walk_func)
    potok_walk.start()

def take_pet_out():
    global need_walk
    bot.send_message(id_chata.chat_id, "Ваш питомец хочет на улицу.")
    need_walk = True
    global last_time_walk
    last_time_walk = time.time()
    create_potok_walk(whaiting_walk)



def check_wash():
    global need_wash
    if need_wash is False:
        bot.send_message(id_chata.chat_id, "Ура, мы чистюли!")
    else:
        bot.send_message(id_chata.chat_id, "Мы свинтусы :(")
        need_wash = False
        get_damage()

def whaiting_wash():
    global last_time_wash
    while time.time() - last_time_wash < 30*60 and need_wash is True:
        time.sleep(1)
    else:
        check_wash()

def create_potok_wash(whaiting_wash_func):
    potok_wash = threading.Thread(target=whaiting_wash_func)
    potok_wash.start()

def wash_pet():
    global need_wash
    bot.send_message(id_chata.chat_id, "Ваш питомец вымазался, его нужно помыть.")
    need_wash = True
    global last_time_wash
    last_time_wash = time.time()
    create_potok_wash(whaiting_wash)



schedule.every(61).minutes.do(feed_pet)
schedule.every(123).minutes.do(take_pet_out)
schedule.every(298).minutes.do(wash_pet)
schedule.every().day.at('03:00').do(check_heel)



def start_life_funktion():
    global pet_health
    pet_health = Health(10)
    while start_life is True:
        schedule.run_pending()
        time.sleep(1)