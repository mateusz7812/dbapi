import copy
from unittest import TestCase

from Objects.DataObjectInterface import DataObject
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

        dataObject = DataObject(data["object"])
        accountObject = DataObject(data["account"])
        request = BasicRequest(accountObject, dataObject, data["action"])

        self.assertEqual(request.account.data, {})
        self.assertEqual(request.account.type, "anonymous")
        self.assertEqual(request.object.type, "account")
        self.assertEqual(request.object.data, {"login": "test", "password": "test"})
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

        dataObject = DataObject(data["object"])
        accountObject = DataObject(data["account"])
        expected_request = BasicRequest(accountObject, dataObject, data["action"])

        self.assertEqual(expected_request.account.data, request.account.data)
        self.assertEqual(expected_request.account.type, request.account.type)
        self.assertEqual(expected_request.object.type, request.object.type)
        self.assertEqual(expected_request.object.data, request.object.data)
        self.assertEqual(expected_request.action, request.action)
