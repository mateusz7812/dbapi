from unittest import TestCase

from DBManager import DBExecutor


class TestDBExecutor(TestCase):
    def test_users(self):
        database = DBExecutor("test")
        self.assertEqual("127.0.0.1", database.address)
        self.assertEqual("password", database.password)
        self.assertEqual("user", database.user)
