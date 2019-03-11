from unittest import TestCase


from DBManager import UsersDBManager
from DataBaseExecutors import TextBExecutor


class TestDBUserManager(TestCase):
    def test_UsersDBManager_add(self):
        TextBExecutor().delete("users", {"login": "test1"})
        TextBExecutor().delete("users", {"login": "test1"})

        user_id = UsersDBManager(TextBExecutor()).add({"login": "test1", "password": "test2", "nick": "nick", "salt": 1234})

        response = UsersDBManager(TextBExecutor()).add({"login": "test1", "password": "test2", "nick": "nick", "salt": 1234})
        self.assertEqual(-1, response)

        filtered_user = TextBExecutor().get("users", {"nick": "nick", "login": "test1"})
        self.assertEqual(["nick", "test1"], filtered_user[0][1:])

        filtered_salt = TextBExecutor().get("salts", {"user_id": user_id})
        self.assertEqual(1234, filtered_salt[0][2])

        filtered_passwords = TextBExecutor().get("passwords", {"user_id": user_id})
        self.assertTrue(filtered_passwords)

    def test_UsersDBManager_get(self):
        logg = UsersDBManager(["test1", "test2"]).get()
        self.assertEqual(self.queryData[0][0], "test1")
        self.assertEqual(self.queryData[1][0], 10)
        self.assertEqual(self.queryData[2][0], 10)

    def test_UsersDBManager_delete(self):
        result = UsersDBManager(["test1", "test2"], self.TDBexec).delete()
        self.assertEqual(self.queryData[0][0], "test1")
        [self.assertEqual(self.queryData[x][0], 10) for x in range(1, 7)]
