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
        self.processor.manager = self.manager

        self.new_response = BasicResponse("", BasicRequest({"id": 1, "login": "login", "password": "password"}, {}, ""))

    def test_Processor(self):
        self.assertEqual("list", self.processor.name)

    def test_add(self):
        self.new_response.request.object = {"type": 'list', "name": "name",
                                            "content": json.dumps(["buy milk", "drink milk", "repeat"])}
        self.new_response.request.action = "add"

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('add', {"id": 1, "user_id": 1, "name": "name",
                                                       "content": json.dumps(["buy milk", "drink milk", "repeat"])})

    def test_add_get_id(self):
        self.new_response.request.object = {"type": 'list', "name": "name",
                                            "content": json.dumps(["buy milk", "drink milk", "repeat"])}
        self.new_response.request.action = "add"

        def manage(action, data):
            if action == "get":
                if data == {'user_id': 1, 'name': 'name'}:
                    return []
                return [{"id": 1, "user_id": 1, "name": "other",
                         "content": json.dumps(["buy milk", "drink milk",
                                                "repeat"])}]

        self.manager.manage.side_effect = manage

        taken_response = self.processor.process(self.new_response)
        self.assertEqual("handled", taken_response.status)

        self.manager.manage.assert_called_with('add', {"id": 2, "user_id": 1, "name": "name",
                                                       "content": json.dumps(
                                                           ["buy milk", "drink milk", "repeat"])})

    def test_add_same_name(self):
        self.new_response.request.action = "add"
        self.new_response.request.object = {"type": 'list', "name": "name",
                                            "content": json.dumps(["buy milk", "drink milk", "repeat"])}
        self.manager.manage.return_value = [{"id": 1, "user_id": 1, "name": "name",
                                             "content": json.dumps(["buy milk", "drink milk", "repeat"])}]

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("failed", taken_response.status)
        self.manager.manage.assert_called_once_with("get", {"user_id": 1, "name": "name"})
        self.assertEqual("taken name", taken_response.result["error"])

    def test_get(self):
        self.new_response.request.object = {"type": 'list', "name": "name",
                                            "content": json.dumps(["buy milk", "drink milk", "repeat"])}
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
        self.new_response.request.object = {"type": 'list', "name": "name",
                                            "content": json.dumps(["buy milk", "drink milk", "repeat"])}
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

    def test_no_name(self):
        self.new_response.request.action = "add"
        self.new_response.request.object = {"type": 'list',
                                            "content": json.dumps(["buy milk", "drink milk", "repeat"])}
        new_prepared_response = copy.deepcopy(self.new_response)

        taken_response = self.processor.process(new_prepared_response)

        self.assertEqual("failed", taken_response.status)
        self.assertEqual("name not found", taken_response.result["error"])
        self.manager.manage.assert_not_called()
