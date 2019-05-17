import copy
import json
from unittest import TestCase
from unittest.mock import Mock

from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Responses.BasicResponse import BasicResponse
from Processors.ListProcessor import ListProcessor

processor = ListProcessor
requestsGenerator = BasicRequestGenerator


class TestListProcessor(TestCase):
    def setUp(self):
        self.processor = processor(requestsGenerator)

        self.manager = Mock()
        self.manager.name = "list"
        self.manager.manage.return_value = []
        self.processor.add_manager(self.manager)

        self.new_response = BasicResponse("new",
                                          BasicRequest({"type": "user", "login": "test", "password": "test"},
                                                       {"type": 'list', "name": "name", "content": json.dumps(
                                                           ["buy milk", "drink milk", "repeat"])},
                                                       "add"))

        self.new_response.request.required["account"] = {"objects": [{"id": 1, "login": "test", "password": "test"}]}

    def test_Processor(self):
        self.assertEqual("list", self.processor.name)
        self.assertEqual(1, len(self.processor.managers))
        self.assertEqual(requestsGenerator, type(self.processor.request_generator))

    def test_required_requests(self):
        required_requests = self.processor.get_required_requests(self.new_response)

        self.assertEqual(1, len(required_requests))
        self.assertIsInstance(required_requests[0], BasicRequest)
        self.assertEqual("test", required_requests[0].object["login"])
        self.assertEqual("test", required_requests[0].object["password"])

    def test_add(self):
        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('add', {"id": 1, "user_id": 1, "name": "name",
                                                       "content": json.dumps(["buy milk", "drink milk", "repeat"])})

    def test_add_key_instead_of_password(self):
        self.new_response.request.account = {"type": "session", "user_id": 1, "key:": "1233532543543"}
        self.new_response.request.required["account"] = {"objects": [{"id": 1, "login": "test", "password": "test"}]}

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('add', {"id": 1, "user_id": 1, "name": "name",
                                                       "content": json.dumps(["buy milk", "drink milk", "repeat"])})

    def test_add_same_name(self):
        self.manager.manage.return_value = [{"id": 1, "user_id": 1, "name": "name",
                                             "content": json.dumps(["buy milk", "drink milk", "repeat"])}]

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("failed", taken_response.status)
        self.manager.manage.assert_called_once_with("get", {"user_id": 1, "name": "name"})
        self.assertEqual("taken name", taken_response.result["error"])

    def test_get(self):
        self.new_response.request.action = "get"
        self.manager.manage.return_value = [{"id": 1, "user_id": 1, "name": "name",
                                             "content": json.dumps(["buy milk", "drink milk", "repeat"])}]

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('get', {"user_id": 1, "name": "name",
                                                       "content": json.dumps(["buy milk", "drink milk", "repeat"])})
        self.assertIn({"id": 1, "user_id": 1, "name": "name",
                       "content": json.dumps(["buy milk", "drink milk", "repeat"])},
                      taken_response.result["objects"])

    def test_del(self):
        self.new_response.request.action = "del"
        self.manager.manage.return_value = [{"id": 1, "user_id": 1, "name": "name",
                                             "content": json.dumps(["buy milk", "drink milk", "repeat"])}]

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('del', {"user_id": 1, "name": "name",
                                                       "content": json.dumps(["buy milk", "drink milk", "repeat"])})
        self.assertIn({"id": 1, "user_id": 1, "name": "name",
                       "content": json.dumps(["buy milk", "drink milk", "repeat"])},
                      taken_response.result["objects"])

    def test_no_user(self):
        self.new_response.request.required["account"]["objects"] = []

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("failed", taken_response.status)
        self.assertEqual("user not found", taken_response.result["error"])
        self.manager.manage.assert_not_called()

    def test_no_name(self):
        new_prepared_response = copy.deepcopy(self.new_response)
        new_prepared_response.request.object.pop("name")

        taken_response = self.processor.process(new_prepared_response)

        self.assertEqual("failed", taken_response.status)
        self.assertEqual("name not found", taken_response.result["error"])
        self.manager.manage.assert_not_called()
