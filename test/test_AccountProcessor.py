from unittest import TestCase
from unittest.mock import Mock

from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Requests.RequestInterface import Request
from Responses.BasicResponse import BasicResponse
from Processors.AccountProcessor import AccountProcessor

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
        self.assertEqual([], requireds)

    def test_process_add_first(self):

        def ret_func(action, data):
            if action == "get":
                if data == {"login": "test"}:
                    return []
                else:
                    return [{'id': 10, 'login': 'other', 'password': 'test'}]

        self.manager.manage.side_effect = ret_func

        taken_response = self.processor.process(self.response)
        self.assertEqual("handled", taken_response.status)
        self.assertEqual(('add', {"id": 11, 'login': 'test', 'password': 'test'}), self.manager.manage.call_args[0])

    def test_process_add_second(self):
        return_value = []

        def ret_func(action, data):
            if action == "get":
                return return_value

        self.manager.manage.side_effect = ret_func

        taken_response = self.processor.process(self.response)
        self.assertEqual(('add', {"id": 1, 'login': 'test', 'password': 'test'}), self.manager.manage.call_args[0])
        self.assertEqual("handled", taken_response.status)

    def test_process_add_same(self):
        return_value = [{'id': 10, 'login': 'test', 'password': 'test'}]

        def ret_func(action, data):
            if action == "get":
                return return_value

        self.manager.manage.side_effect = ret_func
        taken_response = self.processor.process(self.response)
        self.assertEqual("failed", taken_response.status)
        self.assertEqual("taken login", taken_response.result["error"])

    def test_process_get(self):
        self.response.request.action = "get"
        self.manager.manage.return_value = [{'id': 10, 'login': 'test', 'password': 'test'}]

        taken_response = self.processor.process(self.response)

        self.assertEqual(('get', {'login': 'test', 'password': 'test'}), self.manager.manage.call_args[0])
        self.assertEqual("handled", taken_response.status)
        objects = taken_response.result["objects"]
        self.assertEqual(1, len(objects))
        self.assertEqual("test", objects[0]["login"])
        self.assertEqual("test", objects[0]["password"])
        self.assertEqual(int, type(objects[0]["id"]))

    def test_process_fail(self):
        self.response.request.object.pop("login")
        taken_response = self.processor.process(self.response)
        self.assertFalse(self.manager.manage.called)
        self.assertEqual("failed", taken_response.status)
        self.assertEqual("no login/password", taken_response.result["error"])
