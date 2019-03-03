import unittest
from unittest import TestCase

from BranchInterfaces import DBListMBase
from Branchs import ListsGet, ListAdd, ListDel


class TestListDBManager(DBListMBase):
    def __init__(self, data: []):
        super().__init__(data)

    def add(self):
        if not self.validate():
            return False
        return self.data

    def get(self):
        if not self.validate():
            return False
        return True

    def delete(self):
        if not self.validate():
            return False
        if self.data[0] == 15:
            return True
        return False

    def validate(self):
        return self.user_id == 12 and self.user_key == "key1"


class TestListBranch(TestCase):
    def test_ListsGet_correct(self):
        result = ListsGet(TestListDBManager).process_request([12, "key1"])
        self.assertTrue(result)

    def test_ListsGet_bad_user_key(self):
        result = ListsGet(TestListDBManager).process_request([12, "key2"])
        self.assertFalse(result)

    def test_ListsGet_bad_user_id(self):
        result = ListsGet(TestListDBManager).process_request([10, "key1"])
        self.assertFalse(result)

    def test_ListAdd_correct(self):
        result = ListAdd(TestListDBManager).process_request([12, "key1", "test", "content"])
        self.assertTrue(result)

    def test_ListDel_correct(self):
        result = ListDel(TestListDBManager).process_request([12, "key1", 15])
        self.assertTrue(result)

