import time
import threading
import telebot
import random
from class_bd import get_connection

bot = telebot.TeleBot('6202651990:AAEsQjIPBDqsMOx5wMjdFYEH44kMumWFMsU')



def feed_pet():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET need_food = True")
    conn.commit()

    def feed_potok():
        time.sleep(30 * 60)
        cursor.execute("SELECT * FROM users WHERE need_food = True AND life_status = True")
        result = cursor.fetchall()
        for row in result:
            id = row[0]
            hp = row[5]
            if hp > 1:
                cursor.execute(f"UPDATE users SET need_food = False, need_food_message = False, hp = {hp - 1} WHERE id = {id}")
            else:
                cursor.execute(f"UPDATE users SET need_food = False, need_food_message = False, hp = {hp - 1}, life_status = False WHERE id = {id}")
            bot.send_message(id, "Вы не успели покормить питомца, он теряет 1 здоровье :(")
        conn.commit()

    potok = threading.Thread(target=feed_potok)
    potok.start()


def walk_pet():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET need_walk = True")
    conn.commit()

    def walk_potok():
        time.sleep(30 * 60)
        cursor.execute("SELECT * FROM users WHERE need_walk = True AND life_status = True")
        result = cursor.fetchall()
        for row in result:
            id = row[0]
            hp = row[5]
            if hp > 1:
                cursor.execute(f"UPDATE users SET need_walk = False, need_walk_message = False, hp = {hp - 1} WHERE id = {id}")
            else:
                cursor.execute(f"UPDATE users SET need_walk = False, need_walk_message = False, hp = {hp - 1}, life_status = False WHERE id = {id}")
            bot.send_message(id, "Вы не успели погулять с питомцем, он теряет 1 здоровье :(")
        conn.commit()

    potok = threading.Thread(target=walk_potok)
    potok.start()


def wash_pet():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET need_wash = True")
    conn.commit()

    def wash_potok():
        time.sleep(30 * 60)
        cursor.execute("SELECT * FROM users WHERE need_wash = True AND life_status = True")
        result = cursor.fetchall()
        for row in result:
            id = row[0]
            hp = row[5]
            if hp > 1:
                cursor.execute(f"UPDATE users SET need_wash = False, need_wash_message = False, hp = {hp - 1} WHERE id = {id}")
            else:
                cursor.execute(f"UPDATE users SET need_wash = False, need_wash_message = False, hp = {hp - 1}, life_status = False WHERE id = {id}")
            bot.send_message(id, "Вы не успели погулять с питомцем, он теряет 1 здоровье :(")
        conn.commit()

    potok = threading.Thread(target=wash_potok)
    potok.start()



def check_heel():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users")
    result = cursor.fetchall()
    if result:
        for row in result:
            id = row[0]
            hp = row[5]
            last_hp = row[4]
            if hp < 10:
                if last_hp > hp:
                    cursor.execute(f"UPDATE users SET last_hp = {hp} WHERE id = {id}")
                    conn.commit()
                elif last_hp == hp:
                    cursor.execute(f"UPDATE users SET (last_hp, hp) = ({hp + 1}, {hp + 1}) WHERE id = {id}")
                    conn.commit()
                    bot.send_message(id, 'Вы хорошо следили за питомцем, он чувствует себя замечательно и получает 1 здоровье')



def illness_pet():
    if random.random() <= 0.3:  # 30% случаев
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET illness = True")
        conn.commit()

        def illness_potok():
            time.sleep(30 * 60)
            cursor.execute("SELECT * FROM users WHERE illness = True AND life_status = True")
            result = cursor.fetchall()
            for row in result:
                id = row[0]
                hp = row[5]
                if hp > 3:
                    cursor.execute(f"UPDATE users SET illness = False, illness_message = False, hp = {hp - 3} WHERE id = {id}")
                else:
                    cursor.execute(f"UPDATE users SET illness = False, illness_message = False, hp = {hp - 3}, life_status = False WHERE id = {id}")
                bot.send_message(id, "Вы не вылечили питомца, он теряет 3 здоровье :(")
            conn.commit()

        potok = threading.Thread(target=illness_potok)
        potok.start()