from unittest import TestCase
from DBManager import TextBExecutor, PostgresExecutor


class TestTextBExecutor(TestCase):
    def test_add_to_table(self):
        TextBExecutor("test", {"id": 12, "field": "data"}).delete()
        result = TextBExecutor("test", {"id": 12, "field": "data"}).add(,,
        self.assertEqual([12, "data"], result)

    def test_add_to_table_no_id(self):
        TextBExecutor("test", {"field": "data"}).delete()
        result = TextBExecutor("test", {"field": "data"}).add(,,
        self.assertEqual(int, type(result[0]))
        self.assertEqual("data", result[1])

    def test_add_to_table_taked_id(self):
        TextBExecutor("test", {"id": 12, "field": "data"}).add(,,
        result = TextBExecutor("test", {"id": 12, "field": "data"}).add(,,
        self.assertEqual([], result)

    def test_get_from_table_by_all_data(self):
        TextBExecutor("test", {"id": 12, "field": "data"}).add(,,
        result = TextBExecutor("test", {"id": 12, "field": "data"}).get()
        self.assertIn([12, "data"], result)

    def test_get_from_table_by_id(self):
        TextBExecutor("test", {"id": 12, "field": "data"}).add(,,
        result = TextBExecutor("test", {"id": 12}).get()
        self.assertIn([12, "data"], result)

    def test_get_from_table_by_field(self):
        TextBExecutor("test", {"id": 12, "field": "data"}).add(,,
        result = TextBExecutor("test", {"field": "data"}).get()
        self.assertIn([12, "data"], result)

    def test_delete_from_table(self):
        TextBExecutor("test", {"id": 12, "field": "data"}).add(,,
        result = TextBExecutor("test", {"id": 12, "field": "data"}).delete()
        self.assertEqual(result, [[12, "data"]])


class TestPostgresExecutor(TestCase):
    def test_add_to_table(self):
        result = PostgresExecutor("test", {"field": "data"}).add(,
        self.assertEqual("data", result[1])

    def test_add_to_table_taked_id(self):
        PostgresExecutor("test", {"id": 22, "field": "data"}).add(,
        result = PostgresExecutor("test", {"id": 22, "field": "data"}).add(,
        self.assertEqual([], result)

    def test_get_from_table_by_all_data(self):
        result = PostgresExecutor("test", {"id": 22, "field": "data"}).get()
        self.assertIn([22, "data"], result)

    def test_get_from_table_by_field(self):
        PostgresExecutor("test", {"field": "data"}).add(,
        result = PostgresExecutor("test", {"field": "data"}).get()
        self.assertIn([22, "data"], result)

    def test_delete_from_table(self):
        PostgresExecutor("test", {"field": "other_data"}).add(,
        result = PostgresExecutor("test", {"field": "other_data"}).delete()
        self.assertEqual(result[0][1], "other_data")
