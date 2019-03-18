from unittest import TestCase

from TempDataExecutors import TextTempExecutor


class TestTestTempExecutor(TestCase):
    def setUp(self):
        self.executor = TextTempExecutor()
        import os
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        cur_dir = "\\".join(cur_dir.split("\\")[:-1])
        with open(cur_dir+"\\textDataBases\\temp", "w") as f:
            f.truncate()

    def test_add(self):
        self.executor.add([19, "key2"])
        self.executor.add([99, "key9"])
        self.executor.add([9, "key0"])
        self.assertTrue(self.executor.get([19, "key2"]))
        self.assertTrue(self.executor.get([99, "key9"]))
        self.assertTrue(self.executor.get([9, "key0"]))
        self.assertFalse(self.executor.get([12, "key2"]))

    def test_delete(self):
        self.executor.add([19, "key2"])
        self.assertTrue(self.executor.delete([19, "key2"]))
        self.assertFalse(self.executor.delete([11, "key2"]))
