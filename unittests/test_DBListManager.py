from unittest import TestCase

from DBManager import BaseDExecutor, ListsPostgresManager


class TestConnector:
    def __init__(self, queryData, database):
        self.queryData = queryData
        self.database = database

    def execute(self, operation, parameters=None):
        self.queryData.append(parameters)

    def fetchone(self):
        return [10]

    def fetchall(self):
        return "all"


class TestDBExecutor(BaseDExecutor):
    queryData = []

    def __init__(self, table):
        self.cur = TestConnector(self.queryData, table)

    def end(self):
        pass


class TestDBListManager(TestCase):
    def setUp(self):
        self.queryData = []
        self.TDBexec = TestDBExecutor
        self.queryData = self.TDBexec.queryData

    def tearDown(self):
        self.TDBexec.queryData = []

    def test_DBListManager_add(self):
        result = ListsPostgresManager([12, "key1", "name", "content"], self.TDBexec).add()
        self.assertEqual(self.queryData[0][0], 12)
        self.assertEqual(self.queryData[0][1], "name")
        self.assertEqual(self.queryData[0][2], "content")
        return result

    def test_DBListManager_get(self):
        result = ListsPostgresManager([12, "key1"], self.TDBexec).get()
        self.assertEqual(result, "all")
        self.assertEqual(self.queryData[0][0], 12)

    def test_DBListManager_delete(self):
        result = ListsPostgresManager([12, "key1", 1], self.TDBexec).delete()
        self.assertEqual(self.queryData[0][0], 1)
        self.assertTrue(result)


