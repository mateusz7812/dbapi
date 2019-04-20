from unittest import TestCase

from Objects.DataObjectInterface import DataObject
from Requests.BasicRequest import BasicRequest
from RequestsForwarder.BasicForwarder import BasicForwarder

forwarder = BasicForwarder


class TestForwarder(TestCase):
    def setUp(self):
        self.forwarder = forwarder()

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

    def test_forward(self):

        response =