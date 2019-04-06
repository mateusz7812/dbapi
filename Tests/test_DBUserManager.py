from unittest import TestCase


from WriteManager.DBManager import UsersDBManager
from DataWriter.DataBaseExecutors import TextBExecutor


import os
cur_dir = os.path.dirname(os.path.abspath(__file__))
cur_dir = "\\".join(cur_dir.split("\\")[:-1])


class TestDBUserManager(TestCase):
    def clear_file(self, name):
        with open(cur_dir + "\\DataBaseFiles\\" + name, "r") as f:
            data = f.readline()
        with open(cur_dir + "\\DataBaseFiles\\" + name, "w") as f:
            f.write(data)

    def setUp(self):
        self.executor = TextBExecutor()
        self.clear_file("users")
        self.clear_file("salts")
        self.clear_file("passwords")

    def test_UsersDBManager_add(self):
        user_id = UsersDBManager(self.executor).add({"login": "test1", "password": "test2", "nick": "nick", "salt": 1234})["user_id"]
        response = UsersDBManager(self.executor).add({"login": "test1", "password": "test2", "nick": "nick", "salt": 1234})
        self.assertEqual("took login", response["info"])

        filtered_user = self.executor.get("users", {"nick": "nick", "login": "test1"})
        self.assertEqual("nick", filtered_user[0]["nick"])
        self.assertEqual("test1", filtered_user[0]["login"])

        filtered_salt = self.executor.get("salts", {"user_id": user_id})
        self.assertEqual(1234, filtered_salt[0]["salt"])

        filtered_passwords = self.executor.get("passwords", {"user_id": user_id})
        self.assertTrue(filtered_passwords)

    def test_UsersDBManager_get(self):
        UsersDBManager(self.executor).add({"login": "test1", "password": "test2", "nick": "nick", "salt": 1234})
        result = UsersDBManager(self.executor).check({"login": "test1", "password": "test2"})
        self.assertEqual("user correct", result["info"])
        self.assertEqual(int, type(result["user_id"]))

        result = UsersDBManager(self.executor).check({"login": "test2", "password": "test2"})
        self.assertEqual({"info": "bad login"}, result)

    def test_UsersDBManager_delete(self):
        UsersDBManager(self.executor).add({"login": "test1", "password": "test2", "nick": "nick", "salt": 1234})

        result = UsersDBManager(self.executor).delete({"login": "test1", "password": "test2"})
        self.assertEqual({"info": "user deleted"}, result)

        result = UsersDBManager(self.executor).delete({"login": "test9", "password": "test2"})
        self.assertEqual({"info": "bad login"}, result)
