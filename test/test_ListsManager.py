from unittest import TestCase
from unittest.mock import Mock

from Managers.ListsManager import ListsManager

manager = ListsManager


class TestListsManager(TestCase):
    def setUp(self):
        self.manager = manager()

        self.writer = Mock()
        self.writer.insert.return_value = True
        self.writer.select.return_value = [{"id": 10, "name": "dadasd"}]
        self.writer.delete.return_value = True
        self.writer.prepare.return_value = True
        self.writer.table = "lists"

        self.manager.add_writer(self.writer)

    def test_insert(self):
        result = self.manager.manage("add", {"id": 10, "name": "dadasd"})
        self.assertTrue(self.writer.insert.called)
        self.assertEqual({"id": 10, "name": "dadasd"}, self.writer.insert.call_args[0][0])
        self.assertEqual(True, result)

    def test_get(self):
        result = self.manager.manage("get", {"id": 10})
        self.assertTrue(self.writer.select.called)
        self.assertEqual({"id": 10}, self.writer.select.call_args[0][0])
        self.assertEqual([{"id": 10, "name": "dadasd"}], result)

    def test_delete(self):
        result = self.manager.manage("del", {"id": 10})
        self.assertTrue(self.writer.delete.called)
        self.assertEqual({"id": 10}, self.writer.delete.call_args[0][0])
        self.assertEqual(True, result)

    def test_bad_action(self):
        self.assertRaises(Exception, lambda: self.manager.manage('delete', {"id": 10}))

    def test_add_writer(self):
        # writer adding is in setUp

        self.writer.prepare.assert_called()

