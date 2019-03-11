from unittest import TestCase

from DBManager import DBUserMBase
from RequestProcessor import SessionManager, UsersProcessor, ListsProcessor
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
        self.assertEqual("user logged in", result[0])
        self.assertEqual(12, result[1])
        self.assertEqual("key1", result[2])

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
        self.assertEqual("user logged out", result)

    def test_Session_delete_bad_key(self):
        result = SessionManager([12, "key2"], TestRedisManager).delete()
        self.assertEqual("session not found", result)

    def test_Session_delete_bad_id(self):
        result = SessionManager([10, "key1"], TestRedisManager).delete()
        self.assertEqual("session not found", result)


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


class TestUsersProcessor(TestCase):
    def test_UsersProcessor_add(self):
        result = UsersProcessor(['login', 'password', 'nick'], TestUserDBManager, TestSessionManager).add()
        self.assertEqual("user added", result)

    def test_UsersProcessor_get(self):
        result = UsersProcessor(['login', 'password'], TestUserDBManager, TestSessionManager).get()
        self.assertEqual(19, result[0])

    def test_UsersProcessor_delete(self):
        result = UsersProcessor(['login', 'password', 12345], TestUserDBManager, TestSessionManager).delete()
        self.assertEqual("user deleted", result)


class TestListDBManager(DataManagerBase):

    def add(self):
        return "list added"

    def get(self):
        return "lists gotten"

    def delete(self):
        return "list deleted"


class TestListsProcessor(TestCase):
    def test_ListsProcessor_add(self):
        result = ListsProcessor([12, "key1", 'testowa', 'content'], TestListDBManager).add()
        self.assertEqual("list added", result)

    def test_ListsProcessor_get(self):
        result = ListsProcessor([12, "key1"], TestListDBManager).get()
        self.assertEqual("lists gotten", result)

    def test_UsersProcessor_delete(self):
        result = ListsProcessor([12, "key1", 10], TestListDBManager).delete()
        self.assertEqual("list deleted", result)

