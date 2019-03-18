from unittest import TestCase

from DataBaseExecutors import PostgresExecutor


class TestPostgresConnections(TestCase):
    def test_passwords(self):
        self.exc = PostgresExecutor("passwords")
        self.exc.cur.execute('SELECT * FROM passwords where FALSE')
        self.exc.end()

    def test_lists(self):
        self.exc = PostgresExecutor("lists")
        self.exc.cur.execute('SELECT * FROM lists where FALSE')
        self.exc.end()

    def test_users(self):
        self.exc = PostgresExecutor("users")
        self.exc.cur.execute('SELECT * FROM users where FALSE')
        self.exc.end()

        self.exc = PostgresExecutor("users")
        self.exc.cur.execute('SELECT * FROM salts where FALSE')
        self.exc.end()
