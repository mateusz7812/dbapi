from unittest import TestCase

from DBManager import DBUserMBase
from DataProcessor import SessionManager, DataProcessor
from DataManagerInterface import DataManagerBase
from RedisManager import RedisMBase


class TestRedisManager(RedisMBase):
    key = "key1"
    id = 12

    def add(self):
        self.id = self.user_id
        self.key = self.user_key
        return self.key

    def get(self):
        if self.user_id == self.id and self.user_key == self.key:
            return True
        return False

    def delete(self):
        return True


class SessionTest(TestCase):
    def test_Session_add(self):
        result = SessionManager([12, "key1"], TestRedisManager).add()
        self.assertEqual("key1", result)

    def test_Session_get_correct(self):
        result = SessionManager([12, "key1"], TestRedisManager).get()
        self.assertTrue(result)

    def test_Session_get_bad_key(self):
        result = SessionManager([12, "key2"], TestRedisManager).get()
        self.assertFalse(result)

    def test_Session_get_bad_id(self):
        result = SessionManager([10, "key1"], TestRedisManager).get()
        self.assertFalse(result)

    def test_Session_delete_correct(self):
        result = SessionManager([12, "key1"], TestRedisManager).delete()
        self.assertTrue(result)

    def test_Session_delete_bad_key(self):
        result = SessionManager([12, "key2"], TestRedisManager).delete()
        self.assertFalse(result)

    def test_Session_delete_bad_id(self):
        result = SessionManager([10, "key1"], TestRedisManager).delete()
        self.assertFalse(result)


class TestUserDBManager(DBUserMBase):
    database = []

    def add(self):
        self.database = self.data
        return "user added"

    def get(self):
        if self.login == "login" and self.password == "password":
            return 19
        return False

    def delete(self):
        if self.get():
            return "user deleted"
        return False


class TestSessionManager(DataManagerBase):
    def __init__(self, data):
        self.data = data

    def add(self):
        return self.data

    def get(self):
        if self.data[0] == 19 and self.data[1] == 12345:
            return True
        return False

    def delete(self):
        return "session deleted"


class TestUserDataManager(TestCase):
    def test_DataProcessor_add(self):
        result = DataProcessor(['login', 'password', 'nick'], TestUserDBManager, TestSessionManager).add()
        self.assertEqual("user added", result)

    def test_DataProcessor_get(self):
        result = DataProcessor(['login', 'password'], TestUserDBManager, TestSessionManager).get()
        self.assertEqual(19, result[0])

    def test_DataProcessor_delete(self):
        result = DataProcessor(['login', 'password', 12345], TestUserDBManager, TestSessionManager).delete()
        self.assertEqual("user deleted", result)


