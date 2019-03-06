from unittest import TestCase

from RedisManager import RManager, RedisExecutorBase


class TestRExecutor(RedisExecutorBase):
    data = [12, "key1"]

    def set(self, user_id, user_key):
        self.data[0] = user_id
        self.data[1] = user_key

    def get(self, user_id):
        if user_id == 12:
            return "key1"
        return False

    def delete(self, user_id):
        pass


class TestRManager(TestCase):
    def test_RManager_add(self):
        result = RManager([12, "key1"], TestRExecutor).add()
        self.assertTrue(result)

    def test_RManager_get(self):
        result = RManager([12, "key1"], TestRExecutor).get()
        self.assertTrue(result)

        result = RManager([11, "key1"], TestRExecutor).get()
        self.assertFalse(result)

        result = RManager([12, "key2"], TestRExecutor).get()
        self.assertFalse(result)

    def test_RManager_delete(self):
        result = RManager([12, "key1"], TestRExecutor).delete()
        self.assertTrue(result)
