from unittest import TestCase
from unittest.mock import patch

from Writers.PostgresWriter import PostgresWriter

writer = PostgresWriter


class TestTextWriter(TestCase):

    @patch('psycopg2.connect')
    def test_insert(self, conn):
        self.writer = writer("bad", "postgres", "postgres", "zaq1@WSX", "test")
        self.writer.prepare()

        result = self.writer.insert({"test": '1', "id": 1})

        self.assertTrue(result)
        conn.return_value.cursor.return_value.execute.assert_called_with('INSERT INTO test(test, id) VALUES (\'1\', 1)')

    @patch('psycopg2.connect')
    def test_select(self, conn):
        self.writer = writer("bad", "postgres", "postgres", "zaq1@WSX", "test")
        self.writer.prepare()
        conn.return_value.cursor.return_value.fetchall.return_value = [
            {"test": '1', "id": 1, "data": None, "some_data": None}]

        result = self.writer.select({"test": '1', "id": 1})

        self.assertEqual([{"id": 1, "test": '1'}], result)
        conn.return_value.cursor.return_value.execute.assert_called_with(
            'SELECT * from test where test = \'1\' AND id = 1')

    @patch('psycopg2.connect')
    def test_delete(self, conn):
        self.writer = writer("bad", "postgres", "postgres", "zaq1@WSX", "test")
        self.writer.prepare()
        conn.return_value.cursor.return_value.fetchall.return_value = [
            {"test": 1, "id": 1, "data": None, "some_data": None}]

        result = self.writer.delete({"id": 1})

        self.assertEqual([{"id": 1, "test": 1}], result)
        conn.return_value.cursor.return_value.execute.assert_called_with('DELETE FROM test WHERE id = 1 RETURNING *')
