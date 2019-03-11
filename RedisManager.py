import random
from abc import ABC

import redis

from DataManagerInterface import DataManagerBase


class RedisExecutorBase:
    def __init__(self):
        self.server: redis.Redis = None

    def __get__(self, instance, owner):
        return self.server


class RExecutor(RedisExecutorBase):
    def __init__(self):
        super().__init__()
        self.password = self.get_pass()

        self.server = redis.Redis(
            host='localhost',
            port='6379',
            password=self.password
        )

    def get_pass(self):
        import os
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        with open(cur_dir + "\pass\\rpass") as f:
            data = f.readline()
        return data


class RedisMBase(DataManagerBase):
    def __init__(self, data):
        self.user_id: int = data[0]
        self.user_key: str = data[1]


class RManager(RedisMBase, ABC):
    def __init__(self, data, executor: RedisExecutorBase = RExecutor):
        super().__init__(data)
        self.executor = executor

    def add(self):
        self.exc = self.executor()
        self.exc.set(self.user_id, self.user_key)
        return True

    def get(self):
        self.exc = self.executor()
        if self.user_key == self.exc.get(self.user_id):
            return True
        return False

    def delete(self):
        self.exc = self.executor()
        if self.exc.get(self.user_id):
            self.exc.delete(self.user_id)
            return True
        return "session not found"


class SessionManager(DataManagerBase):
    def __init__(self, task, Rmanager: RedisMBase = RManager):
        self.Rmanager = Rmanager
        self.task = task

    def add(self):
        self.Rmanager = self.Rmanager(self.task)
        self.Rmanager.add(,,
        return [
            "user logged in",
            self.Rmanager.user_id,
            self.Rmanager.user_key
        ]

    def get(self):
        self.Rmanager = self.Rmanager(self.task)
        return self.Rmanager.get()

    def delete(self):
        self.Rmanager = self.Rmanager(self.task)
        if self.Rmanager.get():
            if self.Rmanager.delete():
                return "user logged out"
        return "session not found"
