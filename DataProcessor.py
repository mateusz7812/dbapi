import hashlib
import random

from DBManager import DBUserMBase, UsersPostgresOrganizer
from DataManagerInterface import DataManagerBase
from RedisManager import RedisMBase, RManager


class SessionManager(DataManagerBase):
    def __init__(self, task, Rmanager: RedisMBase = RManager):
        self.Rmanager = Rmanager
        self.task = task

    def add(self):
        self.Rmanager = self.Rmanager(self.task)
        return self.Rmanager.add()

    def get(self):
        self.Rmanager = self.Rmanager(self.task)
        return self.Rmanager.get()

    def delete(self):
        self.Rmanager = self.Rmanager(self.task)
        if self.Rmanager.get():
            return self.Rmanager.delete()
        return False


class DataProcessor(DataManagerBase):
    def __init__(self, data, DBManager: DBUserMBase = UsersPostgresOrganizer, SManager: SessionManager = SessionManager):
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
            return False
        self.SManager = self.SManager([user_id, self.data[2]])
        if self.SManager.get():
            self.SManager.delete()
            return self.DBManager.delete()
        return False
