import random
from abc import ABC

import redis
from Branchs import RedisMBase


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
        with open("rpass") as f:
            data = f.readline()
        return data


class RManager(RedisMBase, ABC):
    def __init__(self, user_id, executor: RedisExecutorBase = RExecutor):
        super().__init__(user_id)
        self.executor = executor

    def add(self):
        user_key = str(random.randInt(0, 1000000))
        with self.executor.__init__() as exc:
            exc.set(self.user_id, user_key)
        self.user_key = user_key
        return True

    def get(self):
        with self.executor.__init__() as exc:
            self.user_key = exc.get(self.user_id)
        return True

    def delete(self):
        with self.executor.__init__() as exc:
            exc.delete(self.user_id)
        return True
