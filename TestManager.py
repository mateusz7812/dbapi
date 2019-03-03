import os
import unittest
import test_BranchHandler
import test_DBListManager
import test_DBUserManager
import test_ListBranch
import test_RManager
import test_UserBranchs

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_UserBranchs))
suite.addTest(loader.loadTestsFromModule(test_ListBranch))
suite.addTest(loader.loadTestsFromModule(test_DBUserManager))
suite.addTest(loader.loadTestsFromModule(test_DBListManager))
suite.addTest(loader.loadTestsFromModule(test_BranchHandler))
suite.addTest(loader.loadTestsFromModule(test_RManager))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
