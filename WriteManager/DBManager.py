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
            return {"info": "took login"}
        value = self.executor.add("users", {"nick": nick, "login": login})
        user_id = value["id"]
        self.executor.add("passwords", {"user_id": user_id, "password": hashed_password})
        self.executor.add("salts", {"user_id": user_id, "salt": salt})
        return {"info": "user added", "user_id": user_id}

    def check(self, data: {}):
        login: str = data["login"]
        password: str = data["password"]
        value = self.executor.get("users", {"login": login})
        if not value:
            return {"info": "bad login"}
        user_id = value[0]["id"]
        value = self.executor.get("salts", {"user_id": user_id})
        salt = value[0]["salt"]
        value = self.executor.get("passwords", {"user_id": user_id})
        hashed_password = value[0]["password"]
        if hashed_password == self.generate_hash(password, salt):
            return {"info": "user correct", "user_id": user_id}
        return {"info": "bad password"}

    def delete(self, data: {}):
        user_correct = self.check(data)
        if user_correct["info"] != "user correct":
            return {"info": user_correct["info"]}
        user_id = user_correct["user_id"]
        self.executor.delete("users", {"id": user_id})
        self.executor.delete("salts", {"user_id": user_id})
        self.executor.delete("passwords", {"user_id": user_id})
        self.executor.delete("lists", {"user_id": user_id})
        return {"info": "user deleted"}


class ListsDBManager:
    def __init__(self, executor):
        self.executor = executor

    def add(self, data):
        user_id = data["user_id"]
        name = data["name"]
        content = data["content"]
        result = self.executor.add("lists", {"user_id": user_id, "name": name, "content": content})
        return {"info": "list added", "id": result["id"]}

    def get(self, data):
        data.pop("user_key")
        lists = self.executor.get("lists", data)
        return {"info": "lists gotten", "lists": lists}

    def delete(self, data):
        lists: dict = self.executor.get("lists", {"user_id": data["user_id"], "name": data["name"]})
        deleted_lists = []
        for list in lists:
            deleted = self.executor.delete("lists", {"id": list["id"]})
            deleted_lists.extend(deleted)
        return {"info": "lists deleted", "lists": deleted_lists}

    def edit(self, data):
        list = self.executor.get("lists", {"id": data.pop("list_id")})[0]
        old_name = list["name"]
        for key in data.keys():
            list[key] = data[key]
        self.add(list)
        self.delete({"user_id": list["user_id"], "name": old_name})
        return {"info": "list edited"}
