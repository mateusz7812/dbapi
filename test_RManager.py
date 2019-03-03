from unittest import TestCase

from RedisManager import RManager, RedisExecutorBase


class TestRExecutor(RedisExecutorBase):
    data = [12, "key1"]

    def set(self, user_id, user_key):
        self.data[0] = user_id
        self.data[1] = user_key

    def get(self, user_id):
        if self.data[0] == user_id:
            return self.data[1]
        return False

    def delete(self, user_id):
        return True


class TestRManager(TestCase):
    def test_add(self):
        result = RManager(12, TestRExecutor)

