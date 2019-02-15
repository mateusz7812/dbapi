import hashlib
import random
import psycopg2


class DBExecutor:
    def __init__(self, database):
        self.conn = None
        self.cur = None
        self.database = database
        self.user, self.password = self.get_pass()

    def get_pass(self):
        with open("dbpass") as f:
            data = f.readlines()
        data = [x.split(":") for x in data]
        for row in data:
            if row[0] == self.database:
                return row[1:]

    def __enter__(self):
        self.conn = psycopg2.connect(host="localhost:5432", database=self.database, user=self.user, password=self.password)
        self.cur = self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()


def register(data):
    login, nick, password = data

    with DBExecutor("users") as exc:
        exc.cur.execute('INSERT INTO users("nick", "login") VALUES(%s, %s)', [nick, login])
        user_id = exc.cur.fetchone()[0]

    salt = random.radint(0, 9999)
    hashed_password = generate_hash(password, salt)

    with DBExecutor("password") as exc:
        exc.cur.execute('INSERT INTO passwords("password", "user_id") VALUES(%s, %s)', hashed_password, user_id)

    with DBExecutor("salts") as exc:
        exc.cur.execute('INSERT INTO salts("salt", "user_id") VALUES(%s, %s)', salt, user_id)
    return True


def login(data):
    login, password = data

    with DBExecutor("users") as exc:
        exc.cur.execute('SELECT id FROM users WHERE login=%s', login)
        user_id = exc.cur.fetchone()[0]

    with DBExecutor("salts") as exc:
        exc.cur.execute('SELECT salt FROM salts WHERE user_id=%s', user_id)
        salt = exc.cur.fetchone()[0]

    with DBExecutor("passwords") as exc:
        exc.cur.execute('SELECT password FROM passwords WHERE user_id=%s', user_id)
        chashed_password = exc.cur.fetchone()[0]

    if chashed_password == generate_hash(password, salt):
        return user_id
    return -1


def get_lists(data):
    user_id = data

    with DBExecutor("lists") as exc:
        exc.cur.execute('SELECT name, content FROM lists WHERE user_id=%s', user_id)
        lists = exc.cur.fetchall()
    return lists


def add_list(data):
    name, content = data

    with DBExecutor("lists") as exc:
        exc.cur.execute('INSERT INTO lists("user_id", "name", "content") VALUES (%s, %s, %s)', [user_id, name, content])
        chashed_password = exc.cur.fetchone()[0]

    return -1


def del_list(data: int):
    list_id = data
    with DBExecutor("lists") as exc:
        exc.cur.execute('DELETE FROM lists WHERE id=%s', list_id)
    return True


def generate_hash(password, salt):
    hasher = hashlib.md5()
    hasher.update(password)
    hasher.update(salt)
    hashed = hasher.hexdigest()
    return hashed
