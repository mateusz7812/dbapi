import hashlib

from BranchInterfaces import DBUserMBase, DBListMBase


class BaseDBExecutor:
    def __init__(self, databaseName):
        self.database = databaseName

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError


class DBExecutor(BaseDBExecutor):
    def __init__(self, database):
        super(DBExecutor, self).__init__(database)
        self.user, self.password = self.get_pass()

    def __enter__(self):
        self.conn = psycopg2.connect(host="192.168.88.111", database=self.database, user=self.user, password=self.password)
        self.cur = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.cur = None
        self.conn.close()
        self.conn = None

    def get_pass(self):
        with open("dbpass") as f:
            data = f.readlines()
        data = [x[:-1].split(":") for x in data]
        for row in data:
            if row[0] == self.database:
                return row[1:]


class DBUserManager(DBUserMBase):
    def __init__(self, data, executor: BaseDBExecutor = DBExecutor):
        self.executor = executor
        super().__init__(data)

    def add(self):
        nick = self.data[0]
        with self.executor.__init__("users") as exc:
            exc.cur.execute('INSERT INTO users("nick", "login") VALUES(%s, %s) RETURNING id', [nick, self.login])
            user_id = exc.cur.fetchone()[0]

        salt = random.randint(0, 9999)
        hashed_password = self.generate_hash(salt)

        with self.executor.__init__("password") as exc:
            exc.cur.execute('INSERT INTO passwords("password", "user_id") VALUES(%s, %s)', hashed_password, user_id)

        with self.executor.__init__("salts") as exc:
            exc.cur.execute('INSERT INTO salts("salt", "user_id") VALUES(%s, %s)', salt, user_id)
        return True

    def get(self):
        with self.executor.__init__("users") as exc:
            exc.cur.execute('SELECT id FROM users WHERE login=%s', self.login)
            user_id = exc.cur.fetchone()[0]

        with self.executor.__init__("salts") as exc:
            exc.cur.execute('SELECT salt FROM salts WHERE user_id=%s', user_id)
            salt = exc.cur.fetchone()[0]

        with self.executor.__init__("passwords") as exc:
            exc.cur.execute('SELECT password FROM passwords WHERE user_id=%s', user_id)
            chashed_password = exc.cur.fetchone()[0]

        if chashed_password == self.generate_hash(salt):
            return user_id
        return False

    def delete(self):
        user_id = self.get()

        if user_id != -1:
            with self.executor.__init__("users") as exc:
                exc.cur.execute('DELETE FROM users WHERE id=$s', user_id)

            with self.executor.__init__("salts") as exc:
                exc.cur.execute('DELETE FROM salts WHERE user_id=%s', user_id)

            with self.executor.__init__("passwords") as exc:
                exc.cur.execute('DELETE FROM passwords WHERE user_id=%s', user_id)

            with self.executor.__init__("lists") as exc:
                exc.cur.execute('DELETE FROM lists WHERE user_id=%s', user_id)

            return user_id
        return False

    def generate_hash(self, salt):
        hasher = hashlib.md5()
        hasher.update(bytes(self.password, "utf-8"))
        hasher.update(salt)
        hashed = hasher.hexdigest()
        return hashed


class DBListManager(DBListMBase):
    def __init__(self, data, executor: BaseDBExecutor = DBExecutor):
        self.executor = executor
        super().__init__(data)

    def add(self):
        name, content = self.data

        with self.executor.__init__("lists") as exc:
            exc.cur.execute('INSERT INTO lists("user_id", "name", "content") VALUES (%s, %s, %s) RETURNING id',
                            [self.user_id, name, content])
            list_id = exc.cur.fetchone()[0]

        return list_id

    def get(self):
        with self.executor.__init__("lists") as exc:
            exc.cur.execute('SELECT name, content FROM lists WHERE user_id=%s', self.user_id)
            lists = exc.cur.fetchall()

        return lists

    def delete(self):
        list_id = self.data
        with self.executor.__init__("lists") as exc:
            exc.cur.execute('DELETE FROM lists WHERE id=%s', list_id)
        return True
