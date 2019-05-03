import copy
from unittest import TestCase
from unittest.mock import patch, Mock

from Requests.BasicRequest import BasicRequest
from RequestsForwarder.BasicForwarder import BasicForwarder
from Responses.BasicResponseGenerator import BasicResponseGenerator

forwarder = BasicForwarder
responseGenerator = BasicResponseGenerator


class TestForwarder(TestCase):
    def setUp(self):
        self.responseGenerator = responseGenerator()
        self.forwarder = forwarder(responseGenerator)

        data_object = {"type": "account",
                       "login": "test",
                       "password": "test"}

        account_object = {"type": "anonymous"}
        self.request = BasicRequest(account_object, data_object, "add")

        def process(response):
            response.status = "handled"
            response.result["user_id"] = 12
            return response

        self.account_processor_mock = Mock()
        self.account_processor_mock.get_required_requests.return_value = []
        self.account_processor_mock.name = "account"
        self.account_processor_mock.process = process

    def test_forward(self):
        self.forwarder.add_processor(self.account_processor_mock)
        result = self.forwarder.forward(self.request)

        self.assertEqual(12, result["user_id"])

    def test_forward_with_required(self):
        def process(response):
            response.status = "handled"
            response.result["user_id"] = response.request.required["account"]["user_id"]
            response.result["user_key"] = "abcdefgh"
            return response

        self.forwarder.add_processor(self.account_processor_mock)
        session_processor_mock = Mock()
        data_object = {"type": "account", "login": "test", "password": "test"}
        account_object = {"type": "anonymous"}
        session_processor_mock.get_required_requests.return_value = [BasicRequest(account_object, data_object, "get")]
        session_processor_mock.process = process
        session_processor_mock.name = "session"
        self.forwarder.add_processor(session_processor_mock)

        self.request.object["type"] = "session"

        result = self.forwarder.forward(self.request)
        self.assertEqual("handled", result["status"])
        self.assertEqual(12, result["user_id"])
        self.assertEqual("abcdefgh", result["user_key"])
