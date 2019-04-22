from unittest import TestCase

from RequestsForwarder.ForwarderInterface import Forwarder
from Objects.DataObjectInterface import DataObject
from Requests.BasicRequest import BasicRequest
from Responses.BasicResponse import BasicResponse
from Responses.BasicResponseGenerator import BasicResponseGenerator

generator = BasicResponseGenerator


class TestBasicResponseGenerator(TestCase):
    def setUp(self):
        self.generator = generator()

        data = {
            "account": {"type": "anonymous"},
            "object": {"type": "account",
                       "login": "test",
                       "password": "test"},
            "action": "add",
        }

        dataObject = DataObject(data["object"])
        accountObject = DataObject(data["account"])
        self.request = BasicRequest(accountObject, dataObject, data["action"])

    def test_response(self):
        response = BasicResponse("new", self.request)

        self.assertEqual("new", response.status)
        self.assertEqual(self.request, response.request)
        self.assertEqual({}, response.result)

    def test_generate(self):
        response = self.generator.generate(self.request)

        self.assertEqual("new", response.status)
        self.assertEqual(self.request, response.request)
        self.assertEqual({}, response.result)
