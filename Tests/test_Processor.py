import os
from unittest import TestCase

from WriteManager.DBManager import UsersDBManager, ListsDBManager
from DataWriter.DataBaseExecutors import TextBExecutor
from TaskProcessor.Processor import UsersProcessor, ListsProcessor
from WriteManager.SessionManager import SessionManager
from DataWriter.TempDataExecutors import TextTempExecutor


def clear_file(name):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    cur_dir = "\\".join(cur_dir.split("\\")[:-1])
    with open(cur_dir + "\\DataBaseFiles\\" + name, "r") as f:
        config = f.readline()
    with open(cur_dir + "\\DataBaseFiles\\" + name, "w") as f:
        f.truncate()
        f.write(config)


class TestUsersProcessor(TestCase):
    def setUp(self):
        clear_file("users")
        clear_file("salts")
        clear_file("passwords")
        clear_file("temp")
        self.usersDBM = UsersDBManager(TextBExecutor())
        self.sessionM = SessionManager(TextTempExecutor())
        self.usersP = UsersProcessor(self.usersDBM, self.sessionM)

    def test_UsersProcessor_register(self):
        result = self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})

        self.assertIn(result["info"], ["user added", "took login"])

    def test_UsersProcessor_login(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})

        result = self.usersP.login({"login": 'login', "password": 'password'})

        self.assertEqual("session added", result["info"])

    def test_UsersProcessor_logout(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        session_created = self.usersP.login({"login": 'login', "password": 'password'})
        user_id = session_created["user_id"]
        user_key = session_created["user_key"]

        result = self.usersP.logout({"user_id": user_id, "user_key": user_key})

        self.assertEqual("session deleted", result["info"])

    def test_UsersProcessor_delete(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]
        user_key = user_gotten["user_key"]

        result = self.usersP.delete({"login": 'login', "password": 'password', "user_key": user_key, "user_id": user_id})

        self.assertEqual("user deleted", result["info"])


class TestListsProcessor(TestCase):
    def setUp(self):
        clear_file("users")
        clear_file("salts")
        clear_file("passwords")
        clear_file("temp")
        clear_file("lists")
        self.listsDBM = ListsDBManager(TextBExecutor())
        self.sessionM = SessionManager(TextTempExecutor())
        self.listsP = ListsProcessor(self.listsDBM, self.sessionM)
        self.usersDBM = UsersDBManager(TextBExecutor())
        self.usersP = UsersProcessor(self.usersDBM, self.sessionM)

    def test_ListsProcessor_add(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]
        user_key = user_gotten["user_key"]

        result = self.listsP.add({"user_id": user_id, "user_key": user_key, "name": 'testowa', "content": 'content'})

        self.assertEqual("list added", result["info"])

    def test_ListsProcessor_add_bad_key(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]

        user_key = "bad key"
        result = self.listsP.add({"user_id": user_id, "user_key": user_key, "name": 'testowa', "content": 'content'})

        self.assertEqual("session not correct", result["info"])

    def test_ListsProcessor_get_empty(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]
        user_key = user_gotten["user_key"]

        result = self.listsP.get({"user_id": user_id, "user_key": user_key})

        self.assertEqual("lists gotten", result["info"])
        self.assertEqual([], result["lists"])

    def test_ListsProcessor_get_filled(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]
        user_key = user_gotten["user_key"]
        self.listsP.add({"user_id": user_id, "user_key": user_key, "name": 'testowa', "content": 'content'})

        result = self.listsP.get({"user_id": user_id, "user_key": user_key})

        self.assertEqual("lists gotten", result["info"])
        self.assertEqual(1, len(result["lists"]))

    def test_ListsProcessor_get_bad_key(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]

        user_key = "bad key"
        result = self.listsP.get({"user_id": user_id, "user_key": user_key})

        self.assertEqual("session not correct", result["info"])

    def test_ListsProcessor_delete(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]
        user_key = user_gotten["user_key"]
        added_list = self.listsP.add({"user_id": user_id, "user_key": user_key, "name": 'testowa', "content": 'content'})
        list_id = added_list["id"]

        result = self.listsP.delete({"user_id": user_id, "user_key": user_key, "list_id": list_id})

        self.assertEqual("lists deleted", result["info"])
        self.assertEqual(1, len(result["lists"]))

    def test_ListsProcessor_delete_bad_key(self):
        self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        user_gotten = self.usersP.login({"login": 'login', "password": 'password', "nick": 'nick'})
        user_id = user_gotten["user_id"]
        user_key = user_gotten["user_key"]
        added_list = self.listsP.add({"user_id": user_id, "user_key": user_key, "name": 'testowa', "content": 'content'})
        list_id = added_list["id"]

        user_key = "bad key"
        result = self.listsP.delete({"user_id": user_id, "user_key": user_key, "list_id": list_id})

        self.assertEqual("session not correct", result["info"])

