import os
from unittest import TestCase

from DBManager import ListsDBManager
from DataBaseExecutors import TextBExecutor

cur_dir = os.path.dirname(os.path.abspath(__file__))
cur_dir = "\\".join(cur_dir.split("\\")[:-1])


class TestDBListManager(TestCase):
    def setUp(self):
        executor = TextBExecutor()
        self.listsM = ListsDBManager(executor)
        with open(cur_dir + "\\textDataBases\\" + "lists", "r") as f:
            data = f.readline()
        with open(cur_dir + "\\textDataBases\\" + "lists", "w") as f:
            f.write(data)

    def test_DBListManager_add(self):
        result = self.listsM.add({"user_id": 12, "name": "name", "content": "content"})
        self.assertEqual(result["info"], "list added")
        self.assertEqual(type(result["id"]), int)

    def test_DBListManager_get(self):
        self.listsM.add({"user_id": 12, "name": "name", "content": "content"})
        result = self.listsM.get({"user_id": 12})
        self.assertEqual(result["info"], "lists gotten")
        self.assertEqual(result["lists"][0]["user_id"], 12)

    def test_DBListManager_delete(self):
        self.listsM.add({"user_id": 12, "name": "name", "content": "content"})
        result = self.listsM.delete({"user_id": 12, "name": "name"})
        self.assertEqual("lists deleted", result["info"])
        self.assertEqual(1, len(result["lists"]))
        self.assertEqual("name", result["lists"][0]["name"])
        self.assertEqual("content", result["lists"][0]["content"])

        result = self.listsM.get({"user_id": 12})
        self.assertEqual(result["info"], "lists gotten")
        self.assertEqual(len(result["lists"]), 0)

