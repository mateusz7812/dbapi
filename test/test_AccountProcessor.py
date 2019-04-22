from unittest import TestCase
from unittest.mock import Mock

from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Requests.RequestInterface import Request
from Responses.BasicResponse import BasicResponse
from TaskProcessor.AccountProcessor import AccountProcessor

processor = AccountProcessor
requestsGenerator = BasicRequestGenerator


class TestAccountProcessor(TestCase):
    def setUp(self):
        self.processor = processor(requestsGenerator)

        self.manager = Mock()
        self.manager.name = "account"
        self.manager.manage.return_value = True
        self.processor.add_manager(self.manager)

        self.response = BasicResponse("new",
                                      BasicRequest({"type": "anonymous"},
                                                   {"type": "account", "login": "test", "password": "test"},
                                                   "add"))

    def test_Account(self):
        self.assertEqual("account", self.processor.name)
        self.assertEqual(1, len(self.processor.managers))
        self.assertEqual(requestsGenerator, type(self.processor.request_generator))

    def test_get_required_requests(self):
        requireds = self.processor.get_required_requests(self.response)
        self.assertEqual([], requireds)

        self.response.request.action = "get"
        requireds = self.processor.get_required_requests(self.response)
        self.assertEqual([], requireds)

        self.response.request.action = "del"
        requireds = self.processor.get_required_requests(self.response)

        self.assertEqual(1, len(requireds))
        prepared_request = BasicRequest({"type": "internal"},
                                        {"type": "account", "login": "test", "password": "test"},
                                        "get")
        self.assertTrue(isinstance(requireds[0], Request))
        self.assertEqual(prepared_request.action, requireds[0].action)

    def test_process(self):
        taken_response = self.processor.process(self.response)
        self.assertEqual(('add', {'login': 'test', 'password': 'test'}), self.manager.manage.call_args[0])
        self.assertEqual("handled", taken_response.status)

    def test_process_fail(self):
        self.response.request.object.pop("login")
        taken_response = self.processor.process(self.response)
        self.assertFalse(self.manager.manage.called)
        self.assertEqual("failed", taken_response.status)
        self.assertEqual("no login/password", taken_response.result["error"])
