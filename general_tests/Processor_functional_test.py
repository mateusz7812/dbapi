import os
from unittest import TestCase

from DBManager import UsersDBManager, ListsDBManager
from DataBaseExecutors import TextBExecutor
from Processor import UsersProcessor, ListsProcessor
from TempDataExecutors import TextTempExecutor
from SessionManager import SessionManager


def clear_file(name):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    cur_dir = "\\".join(cur_dir.split("\\")[:-1])
    with open(cur_dir + "\\textDataBases\\" + name, "r") as f:
        config = f.readline()
    with open(cur_dir + "\\textDataBases\\" + name, "w") as f:
        f.truncate()
        f.write(config)


class TestServer(TestCase):
    def setUp(self):
        clear_file("users")
        clear_file("salts")
        clear_file("passwords")
        clear_file("temp")
        clear_file("lists")
        dataWriter = TextBExecutor()
        usersDBM = UsersDBManager(dataWriter)
        listsDBM = ListsDBManager(dataWriter)
        sessionWriter = TextTempExecutor()
        sessionsM = SessionManager(sessionWriter)
        self.usersP = UsersProcessor(usersDBM, sessionsM)
        self.listsP = ListsProcessor(listsDBM, sessionsM)

    def test_new_user_procedure(self):
        # user is being registered
        result = self.usersP.register({"login": 'login', "password": 'password', "nick": 'nick'})
        self.assertEqual(result["info"], "user added")

        # user is being logged in
        result = self.usersP.login({"login": 'login', "password": 'password'})
        self.assertEqual(result["info"], "session added")
        self.assertEqual(int, type(result["user_id"]))
        self.assertEqual(str, type(result["user_key"]))
        user_id = result["user_id"]
        user_key = result["user_key"]

        # lists are being showed
        result = self.listsP.get({"user_id": user_id, "user_key": user_key})
        self.assertEqual(result["info"], "lists gotten")
        self.assertEqual(result["lists"], [])

        # list is being added
        result = self.listsP.add({"user_id": user_id, "user_key": user_key, "name": 'testowa', "content": 'testowy'})
        self.assertEqual(result["info"], "list added")
        self.assertEqual(int, type(result["id"]))
        list_id = result["id"]

        # added list exist is being checked
        result = self.listsP.get({"user_id": user_id, "user_key": user_key})
        self.assertEqual(result["info"], "lists gotten")
        self.assertEqual(len(result["lists"]), 1)
        self.assertEqual(result["lists"][0]["name"], "testowa")
        self.assertEqual(result["lists"][0]["content"], "testowy")

        # list is being deleted
        result = self.listsP.delete({"user_id": user_id, "user_key": user_key, "list_id": list_id})
        self.assertEqual(result["info"], "lists deleted")

        # lists are being showed
        result = self.listsP.get({"user_id": user_id, "user_key": user_key})
        self.assertEqual(result["info"], "lists gotten")
        self.assertEqual(result["lists"], [])

        # user is being logged out
        result = self.usersP.logout({"user_id": user_id, "user_key": user_key})
        self.assertEqual(result["info"], "session deleted")

        # list is being added, but it end bad
        result = self.listsP.get({"user_id": user_id, "user_key": user_key, "name": 'testowa', "content": 'content'})
        self.assertEqual(result["info"], "session not correct")

        # user is being logged in
        result = self.usersP.login({"login": 'login', "password": 'password'})
        self.assertEqual(result["info"], "session added")
        self.assertEqual(int, type(result["user_id"]))
        self.assertEqual(str, type(result["user_key"]))
        user_id = result["user_id"]
        user_key = result["user_key"]

        # user is being deleted
        result = self.usersP.delete({"user_id": user_id, "user_key": user_key, "login": 'login', "password": 'password'})
        self.assertEqual(result["info"], "user deleted")
