from unittest import TestCase

from Writers.PostgresWriter import PostgresWriter

writer = PostgresWriter


class TestTextWriter(TestCase):
    def setUp(self):
        self.writer = writer("localhost", "test", "root", "", "test")

    @patch('builtins.open', new_callable=mock_open())
    def test_insert(self, m):

        result = self.writer.insert({"id": 10, "data": "asdfgdsa"})

        self.assertTrue(result)
        self.assertEqual(("data/test", "a",), m.call_args[0])
        self.assertEqual((json.dumps({"id": 10, "data": "asdfgdsa"}) + "\n",),
                         m.return_value.__enter__.return_value.write.call_args[0])

    @patch('builtins.open', new_callable=mock_open())
    def test_select(self, m):
        m.return_value.__enter__.return_value.readlines.return_value = [
            json.dumps({"id": 10, "data": "asdfgdsa"}) + "\n", json.dumps({"id": 19, "data": "fgsdga"}) + "\n"]

        result = self.writer.select({"id": 10})

        self.assertEqual([{"id": 10, "data": "asdfgdsa"}], result)
        self.assertEqual(("data/test", "r",), m.call_args[0])

    @patch('builtins.open', new_callable=mock_open())
    def test_select_second(self, m):
        m.return_value.__enter__.return_value.readlines.return_value = []

        result = self.writer.select({})

        self.assertEqual([], result)
        self.assertEqual(("data/test", "r",), m.call_args[0])

    @patch('builtins.open', new_callable=mock_open())
    def test_delete(self, m):
        m.return_value.__enter__.return_value.readlines.return_value = [
            json.dumps({"id": 10, "data": "asdfgdsa"}) + "\n", json.dumps({"id": 19, "data": "fgsdga"}) + "\n"]

        result = self.writer.delete({"id": 10})

        m.return_value.__enter__.return_value.readlines.assert_called()
        m.return_value.__enter__.return_value.write.assert_called_once_with(json.dumps({"id": 19, "data": "fgsdga"}) + "\n")
        self.assertEqual([{"id": 10, "data": "asdfgdsa"}], result)
        self.assertEqual([("data/test", "r",), ("data/test", "w",)], [tuple(args[0]) for args in m.call_args_list])

