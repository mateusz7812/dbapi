import hashlib
import random


class BasicProcessor:
    object = None

    def add(self, data):
        raise NotImplementedError

    def get(self, data):
        raise NotImplementedError

    def delete(self, data):
        raise NotImplementedError


class UsersProcessor(BasicProcessor):
    object = "user"

    def __init__(self, DBManager, SManager):
        self.DBManager = DBManager
        self.SManager = SManager

    def register(self, data):
        salt = random.randint(1000, 9999)
        data["salt"] = salt
        return self.DBManager.add(data)

    def login(self, data):
        user_id = self.DBManager.check(data)["user_id"]
        user_number_key = str(random.randint(10000000, 99999999))
        user_key = hashlib.md5(bytes(user_number_key, "utf-8")).hexdigest()
        return self.SManager.add([user_id, user_key])

    def logout(self, data):
        return self.SManager.delete([data["user_id"], data["user_key"]])

    def delete(self, data):
        user_correct = self.DBManager.check(data)
        if user_correct["info"] != "user correct":
            return {"info": "data incorrect"}
        session_correct = self.SManager.delete([data["user_id"], data["user_key"]])["info"]
        if session_correct == "session deleted":
            return {"info": self.DBManager.delete(data)["info"]}
        return {"info": session_correct}


class ListsProcessor(BasicProcessor):
    object = "list"

    def __init__(self, DBManager, SManager):
        self.DBManager = DBManager
        self.SManager = SManager

    def check(self, data):
        user_id = data["user_id"]
        user_key = data["user_key"]
        return self.SManager.get([user_id, user_key])["info"]

    def add(self, data):
        session_confirmed = self.check(data)
        if session_confirmed == "session correct":
            return self.DBManager.add(data)
        return {"info": session_confirmed}

    def get(self, data):
        session_confirmed = self.check(data)
        if session_confirmed == "session correct":
            return self.DBManager.get(data)
        return {"info": session_confirmed}

    def delete(self, data):
        session_confirmed = self.check(data)
        if session_confirmed == "session correct":
            return self.DBManager.delete(data)
        return {"info": session_confirmed}

    def edit(self, data):
        session_confirmed = self.check(data)
        if session_confirmed == "session correct":
            return self.DBManager.edit(data)
        return {"info": session_confirmed}


