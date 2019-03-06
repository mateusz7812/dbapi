from unittest import TestCase

from DBManager import DBExecutor


class TestDatabasesConnections(TestCase):
    def test_passwords(self):
        self.exc = DBExecutor("passwords")
        self.exc.cur.execute('SELECT * FROM passwords where FALSE')
        self.exc.end()

    def test_lists(self):
        self.exc = DBExecutor("lists")
        self.exc.cur.execute('SELECT * FROM lists where FALSE')
        self.exc.end()

    def test_users(self):
        self.exc = DBExecutor("users")
        self.exc.cur.execute('SELECT * FROM users where FALSE')
        self.exc.end()

        self.exc = DBExecutor("users")
        self.exc.cur.execute('SELECT * FROM salts where FALSE')
        self.exc.end()
