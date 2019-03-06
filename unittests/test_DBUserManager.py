from unittest import TestCase


from DBManager import BaseDBExecutor, UsersPostgresOrganizer


class TestConnector:
    def __init__(self, queryData, database):
        self.queryData = queryData
        self.database = database

    def execute(self, operation, parameters=None):
        self.queryData.append(parameters)

    def fetchone(self):
        if self.database == "passwords":
            return [UsersPostgresOrganizer(["test1", "test2"], TestDBExecutor).generate_hash(1111)]
        if self.database == "salts":
            return [1111]
        return [10]


class TestDBExecutor(BaseDBExecutor):
    queryData = []

    def __init__(self, database):
        super().__init__(database)
        self.cur = TestConnector(self.queryData, database)

    def end(self):
        pass


class TestDBUserManager(TestCase):
    def setUp(self):
        self.queryData = []
        self.TDBexec = TestDBExecutor
        self.queryData = self.TDBexec.queryData

    def tearDown(self):
        self.TDBexec.queryData = []

    def test_UsersOrganiser_add(self):
        result = UsersPostgresOrganizer(["test1", "test2", "nick", 1234], self.TDBexec).add()
        self.assertEqual(self.queryData[0], ["nick", "test1"])
        self.assertEqual(self.queryData[1][1], 10)
        self.assertEqual(self.queryData[1][1], 10)
        self.assertTrue(result)

    def test_UsersOrganiser_get(self):
        UsersPostgresOrganizer(["test1", "test2"], self.TDBexec).get()
        self.assertEqual(self.queryData[0][0], "test1")
        self.assertEqual(self.queryData[1][0], 10)
        self.assertEqual(self.queryData[2][0], 10)

    def test_UsersOrganiser_delete(self):
        result = UsersPostgresOrganizer(["test1", "test2"], self.TDBexec).delete()
        self.assertEqual(self.queryData[0][0], "test1")
        [self.assertEqual(self.queryData[x][0], 10) for x in range(1, 7)]
