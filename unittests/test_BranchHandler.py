import unittest

from Branchs import TaskHandler, BaseBranch


class TestBranch1(BaseBranch):
    name = "test1"

    def process_request(self, task):
        return [self.name] + task


class TestBranch2(BaseBranch):
    name = "test2"

    def process_request(self, task):
        return [self.name] + task


class TestBranch3(BaseBranch):
    name = "test3"

    def process_request(self, task):
        return [self.name] + task


class TestBranchHandler(unittest.TestCase):
    def setUp(self):
        self.handler = TaskHandler([])

    def test_BranchHandler_one_branch_routing(self):
        self.handler.add_branchs([TestBranch1])
        result = self.handler.process_request(["test1", "some data"])
        self.assertEqual(result, ["test1", "some data"])

    def test_BranchHandler_more_branches_routing(self):
        self.handler.add_branchs([TestBranch1, TestBranch2, TestBranch3])
        result = self.handler.process_request(["test2", "some data"])
        self.assertEqual(result, ["test2", "some data"])

