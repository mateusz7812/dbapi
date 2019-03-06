import unittest
from unittests import test_UserBranchs, test_DBUserManager, test_ListBranch, test_DBListManager, test_BranchHandler, \
    test_RManager, test_DataManager, test_DBExecutor

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_UserBranchs))
suite.addTest(loader.loadTestsFromModule(test_ListBranch))
suite.addTest(loader.loadTestsFromModule(test_DBUserManager))
suite.addTest(loader.loadTestsFromModule(test_DBListManager))
suite.addTest(loader.loadTestsFromModule(test_BranchHandler))
suite.addTest(loader.loadTestsFromModule(test_RManager))
suite.addTest(loader.loadTestsFromModule(test_DataManager))
suite.addTest(loader.loadTestsFromModule(test_DBExecutor))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
