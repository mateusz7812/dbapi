import abc
import hashlib


class BaseDExecutor(abc.ABC):
    def __init__(self):
        self.tableName: str = ""
        self.data: {} = {}

    def add(self, tableName, requestData):
        raise NotImplementedError

    def get(self, tableName, requestData):
        raise NotImplementedError

    def delete(self, tableName, requestData):
        raise NotImplementedError


class UsersDBManager:
    def __init__(self, executor):
        self.executor = executor
        self.exc: BaseDExecutor

    def generate_hash(self, password, salt):
        hasher = hashlib.md5()
        hasher.update(bytes(password, "utf-8"))
        hasher.update(bytes(str(salt), "utf-8"))
        hashed = hasher.hexdigest()
        return hashed

    def add(self, data: {}):
        login: str = data["login"]
        password: str = data["password"]
        nick: str = data["nick"]
        salt: int = data["salt"]
        hashed_password = self.generate_hash(password, salt)
        if self.executor.get("users", {"login": login}):
            return -1
        user_id = self.executor.add("users", {"nick": nick, "login": login})
        self.executor.add("passwords", {"user_id": user_id, "password": hashed_password})
        self.executor.add("salts", {"user_id": user_id, "salt": salt})
        return user_id

    def get(self, data: {}):
        login: str = data["login"]
        password: str = data["password"]
        value = self.executor.get("users", {"login": login})
        if not value:
            return False

        user_id = value[0]
        salt = self.executor.get("salts", {"user_id": user_id})
        chashed_password = self.executor.get("passwords", {"uer_id": user_id})

        return [user_id if chashed_password == self.generate_hash(password, salt) else False]

    def delete(self, data: {}):
        user_id = self.get(data)
        if user_id == -1:
            return False
        self.executor.delete("users", {"user_id": user_id})
        self.executor.delete("salts", {"user_id": user_id})
        self.executor.delete("passwords", {"user_id": user_id})
        self.executor.delete("lists", {"user_id": user_id})
        return True


class ListsPostgresManager:
    def __init__(self, data, executor):
        self.executor = executor
        super().__init__(data)

    def add(self):
        name, content = self.data
        list_id = self.executor("lists", {"user_id": self.user_id, "name": name, "content": content})
        return list_id

    def get(self):
        lists = self.executor("lists", {"user_id", self.user_id})
        return lists

    def delete(self):
        list_id = self.data[0]
        self.executor("lists", {"list-id": list_id})
        return True
