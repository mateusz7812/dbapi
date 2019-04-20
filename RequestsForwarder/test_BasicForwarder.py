from unittest import TestCase

from Objects.DataObjectInterface import DataObject
from Requests.BasicRequest import BasicRequest
from RequestsForwarder.BasicForwarder import BasicForwarder
from Responses.BasicResponseGenerator import BasicResponseGenerator
from TaskProcessor.ProcessorInterface import Processor

forwarder = BasicForwarder
responseGenerator = BasicResponseGenerator


class ProcessorShape(Processor):
    def get_required_requests(self, response):
        return []

    def process(self, response):
        response.status = "handled"
        return response


class TestForwarder(TestCase):
    def setUp(self):
        self.forwarder = forwarder()
        self.forwarder.add_processor(ProcessorShape("account"))
        self.responseGenerator = responseGenerator()

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
        new_response = self.responseGenerator.generate(self.request)

        handled_response = self.forwarder.forward(new_response)

        self.assertEqual("handled", handled_response.status)

