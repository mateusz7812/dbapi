import hashlib
import random



class UsersProcessor:
    def __init__(self, data, DBManager, SManager):
        self.DBManager = DBManager
        self.SManager = SManager
        self.data = data

    def add(self):
        salt = random.randint(1000, 9999)
        self.data.append(salt)
        self.DBManager = self.DBManager(self.data)
        return self.DBManager.add()

    def get(self):
        self.DBManager = self.DBManager(self.data)
        user_id = self.DBManager.get()
        user_number_key = str(random.randint(10000000, 99999999))
        user_key = hashlib.md5(bytes(user_number_key, "utf-8")).hexdigest()

        self.SManager = self.SManager([user_id, user_key])
        return self.SManager.add()

    def delete(self):
        self.DBManager = self.DBManager(self.data[:2])
        user_id = self.DBManager.get()
        if not user_id:
            return "user not found"
        self.SManager = self.SManager([user_id, self.data[2]])
        if self.SManager.get():
            self.SManager.delete()
            if self.DBManager.delete():
                return "user deleted"
        return "not authorized"


class ListsProcessor(DataManagerBase):

    def __init__(self, data, DBManager: DBListMBase = ListsPostgresManager):
        self.data = data
        self.DBManager = DBManager

    def add(self):
        self.DBManager = self.DBManager()
        return self.DBManager.add(,

    def get(self):
        self.DBManager = self.DBManager()
        return self.DBManager.get()

    def delete(self):
        self.DBManager = self.DBManager()
        return self.DBManager.delete()



