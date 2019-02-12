import hashlib
import random

import psycopg2


class Executor:
    def __init__(self, database):
        self.conn = None
        self.cur = None
        self.database = database

    def __enter__(self):
        self.conn = psycopg2.connect(host="localhost:5432", database=self.database, user="admin", password="admin")
        self.cur = self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()


def register(data):
    login, nick, password = data

    with Executor("users") as exc:
        exc.cur.execute('INSERT INTO users("nick", "login") VALUES(%s, %s)', [nick, login])
        user_id = exc.cur.fetchone()[0]

    salt = random.radint(0, 9999)
    hashed_password = generate_hash(password, salt)

    with Executor("password") as exc:
        exc.cur.execute('INSERT INTO passwords("password", "user_id") VALUES(%s, %s)', hashed_password, user_id)

    with Executor("salts") as exc:
        exc.cur.execute('INSERT INTO salts("salt", "user_id") VALUES(%s, %s)', salt, user_id)
    return True


def login(data):
    login, password = data

    with Executor("users") as exc:
        exc.cur.execute('SELECT id FROM users WHERE login=%s', login)
        user_id = exc.cur.fetchone()[0]

    with Executor("salts") as exc:
        exc.cur.execute('SELECT salt FROM salts WHERE user_id=%s', user_id)
        salt = exc.cur.fetchone()[0]

    with Executor("passwords") as exc:
        exc.cur.execute('SELECT password FROM passwords WHERE user_id=%s', user_id)
        chashed_password = exc.cur.fetchone()[0]

    if chashed_password == generate_hash(password, salt):
        return user_id
    return -1


def add_list(data):
    return -1


def generate_hash(password, salt):
    hasher = hashlib.md5()
    hasher.update(password)
    hasher.update(salt)
    hashed = hasher.hexdigest()
    return hashed
