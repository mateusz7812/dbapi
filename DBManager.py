import hashlib

import psycopg2

from DataManagerInterface import DataManagerBase


class BaseDBExecutor:
    def __init__(self, database):
        self.name = database

    def end(self):
        raise NotImplementedError


class DBExecutor(BaseDBExecutor):
    def __init__(self, database):
        super(DBExecutor, self).__init__(database)
        [self.address, self.user, self.password] = self.get_pass()
        self.conn = psycopg2.connect(host=self.address, database=self.name, user=self.user, password=self.password)
        self.cur = self.conn.cursor()

    def end(self):
        self.cur.close()
        self.cur = None
        self.conn.close()
        self.conn = None

    def get_pass(self):
        import os
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        with open(cur_dir + "\pass\dbpass") as f:
            data = f.readlines()
        data = [x[:-1].split(":") for x in data]
        for row in data:
            if row[0] == self.name:
                return row[1:]


class DBUserMBase(DataManagerBase):
    def __init__(self, data: []):
        self.login: str = data[0]
        self.password: str = data[1]
        self.data: [] = data[2:]


class UsersPostgresOrganizer(DBUserMBase):
    def __init__(self, data, executor: BaseDBExecutor = DBExecutor):
        self.executor = executor
        self.exc: BaseDBExecutor
        super().__init__(data)

    def add(self):
        nick: str = self.data[0]
        salt: int = self.data[1]

        self.exc = self.executor("users")
        self.exc.cur.execute('INSERT INTO users("nick", "login") VALUES(%s, %s) RETURNING id', [nick, self.login])
        user_id = self.exc.cur.fetchone()[0]
        self.exc.end()

        hashed_password = self.generate_hash(salt)

        self.exc = self.executor("passwords")
        self.exc.cur.execute('INSERT INTO passwords("password", "user_id") VALUES(%s, %s)', [hashed_password, user_id])
        self.exc.end()

        self.exc = self.executor("salts")
        self.exc.cur.execute('INSERT INTO salts("salt", "user_id") VALUES(%s, %s)', [salt, user_id])

        return True

    def get(self):
        self.exc = self.executor("users")
        self.exc.cur.execute('SELECT id FROM users WHERE login=%s', [self.login])
        value = self.exc.cur.fetchone()
        if value:
            user_id = value[0]
        else:
            return False

        self.exc = self.executor("salts")
        self.exc.cur.execute('SELECT salt FROM salts WHERE user_id=%s', [user_id])
        salt = self.exc.cur.fetchone()[0]

        self.exc = self.executor("passwords")
        self.exc.cur.execute('SELECT password FROM passwords WHERE user_id=%s', [user_id])
        chashed_password = self.exc.cur.fetchone()[0]

        if chashed_password == self.generate_hash(salt):
            return user_id
        return False

    def delete(self):
        user_id = self.get()

        if user_id != -1:
            self.exc = self.executor("users")
            self.exc.cur.execute('DELETE FROM users WHERE id=$s', [user_id])

            self.exc = self.executor("salts")
            self.exc.cur.execute('DELETE FROM salts WHERE user_id=%s', [user_id])

            self.exc = self.executor("passwords")
            self.exc.cur.execute('DELETE FROM passwords WHERE user_id=%s', [user_id])

            self.exc = self.executor("lists")
            self.exc.cur.execute('DELETE FROM lists WHERE user_id=%s', [user_id])

            return True
        return False

    def generate_hash(self, salt):
        hasher = hashlib.md5()
        hasher.update(bytes(self.password, "utf-8"))
        hasher.update(bytes(str(salt), "utf-8"))
        hashed = hasher.hexdigest()
        return hashed


class DBListMBase(DataManagerBase):
    def __init__(self, data: []):
        self.user_id: int = data[0]
        self.user_key: str = data[1]
        self.data: [] = data[2:]


class DBListManager(DBListMBase):
    def __init__(self, data, executor: BaseDBExecutor = DBExecutor):
        self.executor: BaseDBExecutor = executor
        super().__init__(data)

    def add(self):
        name, content = self.data

        self.exc = self.executor("lists")
        self.exc.cur.execute('INSERT INTO lists("user_id", "name", "content") VALUES (%s, %s, %s) RETURNING id',
                             [self.user_id, name, content])
        list_id = self.exc.cur.fetchone()[0]

        return list_id

    def get(self):
        self.exc = self.executor("lists")
        self.exc.cur.execute('SELECT name, content FROM lists WHERE user_id=%s', [self.user_id])
        lists = self.exc.cur.fetchall()

        return lists

    def delete(self):
        list_id = self.data[0]
        self.exc = self.executor("lists")
        self.exc.cur.execute('DELETE FROM lists WHERE id=%s', [list_id])
        return True
