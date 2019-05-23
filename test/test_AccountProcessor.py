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
        self.processor.manager = self.manager

        self.response = BasicResponse("", BasicRequest({}, {}, ""))

    def test_settings(self):
        self.assertEqual("account", self.processor.name)

    def test_process_add_first(self):
        self.response.request.object = {"type": "account", "login": "test", "password": "test"}
        self.response.request.action = "add"

        def ret_func(action, data):
            if action == "get":
                if data == {"login": "test"}:
                    return []
                else:
                    return [{"id": 10, 'login': 'other', 'password': 'test'}]

        self.manager.manage.side_effect = ret_func

        taken_response = self.processor.process(self.response)
        self.assertEqual("handled", taken_response.status)
        self.assertEqual(('add', {"id": 11, 'login': 'test', 'password': 'test'}), self.manager.manage.call_args[0])

    def test_process_add_get_first_index(self):
        self.response.request.object = {"type": "account", "login": "test", "password": "test"}
        self.response.request.action = "add"
        return_value = []

        def ret_func(action, data):
            if action == "get":
                return return_value

        self.manager.manage.side_effect = ret_func

        taken_response = self.processor.process(self.response)
        self.assertEqual(('add', {"id": 1, 'login': 'test', 'password': 'test'}), self.manager.manage.call_args[0])
        self.assertEqual("handled", taken_response.status)

    def test_process_add_same_login(self):
        self.response.request.action = "add"
        self.response.request.object = {"type": "account", "login": "test", "password": "test"}
        return_value = [{'id': 10, 'login': 'test', 'password': 'test'}]

        def ret_func(action, data):
            if action == "get":
                return return_value

        self.manager.manage.side_effect = ret_func
        taken_response = self.processor.process(self.response)
        self.assertEqual("failed", taken_response.status)
        self.assertEqual("taken login", taken_response.result["error"])

    def test_process_add_same_nick(self):
        self.response.request.object = {"type": "account", "login": "test", "password": "test", "nick": "nick"}
        self.response.request.action = "add"
        return_value = [{'id': 10, 'login': 'other', 'password': 'test', "nick": "nick"}]

        def ret_func(action, data):
            if action == "get":
                if data == {"nick": "nick"}:
                    return return_value
                else:
                    return []

        self.manager.manage.side_effect = ret_func
        taken_response = self.processor.process(self.response)
        self.assertEqual("failed", taken_response.status)
        self.assertEqual("taken nick", taken_response.result["error"])

    def test_process_get(self):
        self.response.request.object = {"type": "account", "login": "test", "password": "test"}
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

    def test_admin_add(self):
        self.response.request.object = {"type": "account", "id": 10, "login": "test", "password": "test",
                                        "account_type": "admin"}
        self.response.request.action = "add"

        def ret_func(action, data):
            if action == "get":
                if data == {"login": "test"}:
                    return []
                elif data == {"account_type": "admin"}:
                    return []
                else:
                    return True

        self.manager.manage.side_effect = ret_func

        taken_response = self.processor.process(self.response)
        self.assertEqual("handled", taken_response.status)
        self.assertEqual(('add', {"id": 10, 'login': 'test', 'password': 'test', "account_type": "admin"}),
                         self.manager.manage.call_args[0])

    def test_admin_add_second_admin(self):
        self.response.request.object = {"type": "account", "id": 10, "login": "test", "password": "test",
                                        "account_type": "admin"}
        self.response.request.action = "add"
        self.response.request.account = {"type": "account"}

        def ret_func(action, data):
            if action == "get":
                if data == {"login": "test"}:
                    return []
                elif data == {"account_type": "admin"}:
                    return [{"id": 1, "login": "other", "password": "test",
                             "account_type": "admin"}]
                else:
                    return True

        self.manager.manage.side_effect = ret_func

        taken_response = self.processor.process(self.response)
        self.assertEqual("failed", taken_response.status)
        self.assertEqual("first admin added", taken_response.result["error"])
