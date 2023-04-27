import sqlite3
import threading

class ConnectionFactory:
    def __init__(self, db_file):
        self._db_file = db_file
        self._local = threading.local()

    def get_connection(self):
        if not hasattr(self._local, 'conn'):
            self._local.conn = sqlite3.connect(self._db_file, check_same_thread=False)
        return self._local.conn


def create_connection_factory(db_file):
    global connection_factory
    connection_factory = ConnectionFactory(db_file)


def get_connection():
    conn = connection_factory.get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY,
                    tipe TEXT,
                    life_status BOOLEAN,
                    life_status_message BOOLEAN,
                    last_hp INTEGER,
                    hp INTEGER,
                    name TEXT,
                    need_food BOOLEAN,
                    need_food_message BOOLEAN,
                    need_walk BOOLEAN,
                    need_walk_message BOOLEAN,
                    need_wash BOOLEAN,
                    need_wash_message BOOLEAN,
                    time INTEGER,
                    illness BOOLEAN,
                    illness_message BOOLEAN)''')
    conn.commit()
    return conn