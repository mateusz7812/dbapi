import copy
from unittest import TestCase

from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorBasic import BasicRequestGenerator

requestGenerator = BasicRequestGenerator


class TestBasicRequestGenerator(TestCase):
    def setUp(self):
        self.generator = requestGenerator()

    def test_request(self):
        data = {
            "account": {"type": "anonymous"},
            "object": {"type": "account",
                       "login": "test",
                       "password": "test"},
            "action": "add",
        }

        dataObject = data["object"]
        accountObject = data["account"]
        request = BasicRequest(accountObject, dataObject, data["action"])

        self.assertEqual(request.account, {"type": "anonymous"})
        self.assertEqual(request.object, {"type": "account", "login": "test", "password": "test"})
        self.assertEqual(request.action, "add")

    def test_generate(self):
        data = {
            "account": {"type": "anonymous"},
            "object": {"type": "account",
                       "login": "test",
                       "password": "test"},
            "action": "add",
        }

        request: BasicRequest = self.generator.generate(copy.deepcopy(data))

        dataObject = data["object"]
        accountObject = data["account"]
        expected_request = BasicRequest(accountObject, dataObject, data["action"])

        self.assertEqual(expected_request.account, request.account)
        self.assertEqual(expected_request.object, request.object)
        self.assertEqual(expected_request.action, request.action)
