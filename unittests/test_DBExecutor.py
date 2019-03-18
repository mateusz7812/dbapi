import os
from unittest import TestCase

from DataBaseExecutors import TextBExecutor, PostgresExecutor


class TestTextBExecutor(TestCase):
    def setUp(self):
        self.executor = TextBExecutor()
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        cur_dir = "\\".join(cur_dir.split("\\")[:-1])
        with open(cur_dir + "\\textDataBases\\" + "test", "r") as f:
            config = f.readline()
        with open(cur_dir + "\\textDataBases\\" + "test", "w") as f:
            f.write(config)

    def test_add_to_table(self):
        result = self.executor.add("test", {"id": 12, "field": "data"})
        self.assertEqual({"id": 12, "field": "data"}, result)

    def test_add_to_table_no_id(self):
        result = self.executor.add("test", {"field": "data"})
        self.assertEqual(int, type(result["id"]))
        self.assertEqual("data", result["field"])

    def test_add_to_table_taked_id(self):
        self.executor.add("test", {"id": 12, "field": "data"})
        result = self.executor.add("test", {"id": 12, "field": "data"})
        self.assertEqual([], result)

    def test_get_from_table_by_all_data(self):
        self.executor.add("test", {"id": 12, "field": "data"})
        result = self.executor.get("test", {"id": 12, "field": "data"})
        self.assertIn({"id": 12, "field": "data"}, result)

    def test_get_from_table_by_id(self):
        self.executor.add("test", {"id": 12, "field": "data"})
        result = self.executor.get("test", {"id": 12})
        self.assertIn({"id": 12, "field": "data"}, result)

    def test_get_from_table_by_field(self):
        self.executor.add("test", {"id": 12, "field": "data"})
        result = self.executor.get("test", {"field": "data"})
        self.assertIn({"id": 12, "field": "data"}, result)

    def test_delete_from_table(self):
        self.executor.add("test", {"id": 12, "field": "data"})
        result = self.executor.delete("test", {"id": 12, "field": "data"})
        self.assertIn({"id": 12, "field": "data"}, result)

        result = self.executor.get("test", {"id": 12})
        self.assertEqual(len(result), 0)


"""
class TestPostgresExecutor(TestCase):
    def test_add_to_table(self):
        result = PostgresExecutor("test", {"field": "data"}).add()
        self.assertEqual("data", result[1])

    def test_add_to_table_taked_id(self):
        PostgresExecutor("test", {"id": 22, "field": "data"}).add()
        result = PostgresExecutor("test", {"id": 22, "field": "data"}).add()
        self.assertEqual([], result)

    def test_get_from_table_by_all_data(self):
        result = PostgresExecutor("test", {"id": 22, "field": "data"}).get()
        self.assertIn([22, "data"], result)

    def test_get_from_table_by_field(self):
        PostgresExecutor("test", {"field": "data"}).add()
        result = PostgresExecutor("test", {"field": "data"}).get()
        self.assertIn([22, "data"], result)

    def test_delete_from_table(self):
        PostgresExecutor("test", {"field": "other_data"}).add()
        result = PostgresExecutor("test", {"field": "other_data"}).delete()
        self.assertEqual(result[0][1], "other_data")
"""