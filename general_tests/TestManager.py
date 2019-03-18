import unittest
from unittests import test_DBUserManager, test_DBListManager, test_SessionManager, test_Processor, test_DBExecutor, \
    test_TempDataExecutor

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(test_DBUserManager))
suite.addTest(loader.loadTestsFromModule(test_DBListManager))
suite.addTest(loader.loadTestsFromModule(test_SessionManager))
suite.addTest(loader.loadTestsFromModule(test_Processor))
suite.addTest(loader.loadTestsFromModule(test_DBExecutor))
suite.addTest(loader.loadTestsFromModule(test_TempDataExecutor))

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
