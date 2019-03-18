from unittest import TestCase

from SessionManager import SessionManager
from TempDataExecutors import TextTempExecutor


class TestSManager(TestCase):
    def setUp(self):
        self.executor = TextTempExecutor()
        import os
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        cur_dir = "\\".join(cur_dir.split("\\")[:-1])
        with open(cur_dir + "\\textDataBases\\temp", "w") as f:
            f.truncate()

    def test_SessionManager_add(self):
        result = SessionManager(self.executor).add([12, "key1"])
        self.assertEqual("session added", result["info"])
        self.assertEqual(int, type(result["user_id"]))
        self.assertEqual(str, type(result["user_key"]))

    def test_SessionManager_get(self):
        SessionManager(self.executor).add([12, "key1"])
        result = SessionManager(self.executor).get([12, "key1"])
        self.assertEqual("session correct", result["info"])

        result = SessionManager(self.executor).get([11, "key1"])
        self.assertEqual("session not correct", result["info"])

        result = SessionManager(self.executor).get([12, "key2"])
        self.assertEqual("session not correct", result["info"])

    def test_SessionManager_delete(self):
        SessionManager(self.executor).add([12, "key1"])
        result = SessionManager(self.executor).delete([12, "key1"])
        self.assertEqual("session deleted", result["info"])

        result = SessionManager(self.executor).delete([43, "key1"])
        self.assertEqual("session not correct", result["info"])
