import time
import threading
from dict_id_chats import user_dict
import telebot
from telebot import types

bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')

from pet import Pet


def feed_pet():
    def feed_potok(key, pet):
        pet.food()
        last_time_food = time.time()
        while time.time() - last_time_food < 60*30:
            time.sleep(1)
        if pet.need_food['need_food'] and pet.life_status['life_status'] == True:
            bot.send_message(key, "Вы не успели покормить питомца, он теряет 1 здоровье :(")
            pet.got_food()
            pet.damage()

    for key, pet in user_dict.items():
        pet.food()
        potok = threading.Thread(target=feed_potok, args=(key, pet,))
        potok.start()



def walk_pet():
    def walk_potok(key, pet):
        pet.walk()
        last_time_walk = time.time()
        while time.time() - last_time_walk < 60*30:
            time.sleep(1)
        if pet.need_walk['need_walk'] and pet.life_status['life_status'] == True:
            bot.send_message(key, "Вы не успели погулять с питомцем, он теряет 1 здоровье :(")
            pet.got_walk()
            pet.damage()

    for key, pet in user_dict.items():
        pet.walk()
        potok = threading.Thread(target=walk_potok, args=(key, pet,))
        potok.start()


def wash_pet():
    def wash_potok(key, pet):
        pet.wash()
        last_time_wash = time.time()
        while time.time() - last_time_wash < 60*30:
            time.sleep(1)
        if pet.need_wash['need_wash'] and pet.life_status['life_status'] == True:
            bot.send_message(key, "Вы не успели помыть питомца, он теряет 1 здоровье :(")
            pet.got_wash()
            pet.damage()

    for key, pet in user_dict.items():
        pet.wash()
        potok = threading.Thread(target=wash_potok, args=(key, pet,))
        potok.start()


def check_heel():
    for key, pet in user_dict.items():
        if pet.hp < 10:
            if pet.last_hp > pet.hp:
                pet.last_hp = pet.hp
            elif pet.last_hp == pet.hp:
                pet.heel()
                pet.last_hp = pet.hp
                bot.send_message(key, 'Вы хорошо следили за питомцем, он чувствует себя замечательно и получает 1 здоровье')



