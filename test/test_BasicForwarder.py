import copy
from unittest import TestCase
from unittest.mock import patch, Mock

from Processors.ProcessorInterface import Processor
from Requests.Request import Request
from Forwarders.Forwarder import Forwarder
from Responses.ResponseGenerator import ResponseGenerator

forwarder = Forwarder
responseGenerator = ResponseGenerator
guard = Mock()


class TestForwarder(TestCase):
    def setUp(self):
        self.responseGenerator = responseGenerator()
        self.forwarder = forwarder(responseGenerator, guard)

        # account_object = {"type": "anonymous"}

        self.request = Request({}, {}, "")

        def process(response):
            response.status = "handled"
            response.result["user_id"] = 12
            return response

        self.account_processor_mock = Mock()
        self.account_processor_mock.get_required_requests.return_value = []
        self.account_processor_mock.name = "account"
        self.account_processor_mock.process = process

    def test_forward(self):
        self.request.object = {"type": "account", "login": "test", "password": "test"}

        def resolve(response):
            response.status = "authorized"
            return response

        self.forwarder.guard.resolve.side_effect = resolve
        self.forwarder.add_processor(self.account_processor_mock)

        result = self.forwarder.forward(self.request)

        self.assertEqual(12, result["user_id"])

    def test_forward_not_authorized(self):
        def resolve(response):
            response.status = "not authorized"
            return response

        self.forwarder.guard.resolve.side_effect = resolve

        result = self.forwarder.forward(self.request)

        self.assertEqual("failed", result["status"])
        self.assertEqual("not authorized", result["error"])

    def test_add_processor_to_guard(self):
        self.forwarder.guard.authorization_methods = ["session"]
        self.forwarder.guard.processors = {}
        session_processor_mock = Mock()
        session_processor_mock.name = "session"

        self.forwarder.add_processor(session_processor_mock)

        self.assertEqual(session_processor_mock, self.forwarder.guard.add_processor.call_args_list[0][0][0])
