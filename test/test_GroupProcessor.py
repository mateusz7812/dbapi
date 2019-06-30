import json
from unittest import TestCase
from unittest.mock import Mock

from Processors.GroupProcessor import GroupProcessor
from Requests.Request import Request
from Requests.RequestGenerator import RequestGenerator
from Responses.Response import BasicResponse

processor = GroupProcessor
requestsGenerator = RequestGenerator


class TestListProcessor(TestCase):
    def setUp(self):
        self.processor = processor(requestsGenerator)

        self.manager = Mock()
        self.manager.name = "test"
        self.manager.manage.return_value = []
        self.processor.manager = self.manager

        self.new_response = BasicResponse("", Request({"id": 1, "login": "login", "password": "password"}, {}, ""))

    def test_add(self):
        self.new_response.request.object = {"type": 'group', "name": "my_group"}
        self.new_response.request.action = "add"

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('add', {"name": "my_group", "admin_id": 1})

    def test_get(self):
        self.new_response.request.object = {"type": 'group', "name": "my_group"}
        self.new_response.request.action = "get"
        self.manager.manage.return_value = [{"id": 1, "name": "my_group", "admin_id": 1}]

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('get', {"name": "my_group"})
        self.assertIn({"id": 1, "name": "my_group", "admin_id": 1},
                      taken_response.result["objects"])

    def test_del(self):
        self.new_response.request.object = {"type": 'group', "id": 1, "name": "my_group"}
        self.new_response.request.action = "del"
        self.manager.manage.return_value = [{"id": 1, "name": "my_group", "admin_id": 1}]

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("handled", taken_response.status)
        call_args_list = list(map(list, self.manager.manage.call_args_list))[0]
        self.assertIn(('get', {"id": 1, "name": "my_group"}), call_args_list)
        self.manager.manage.assert_called_with('del', {"id": 1, "name": "my_group"})
        self.assertIn({"id": 1, "name": "my_group", "admin_id": 1},
                      taken_response.result["objects"])

    def test_del_bad_account_id(self):
        self.new_response.request.object = {"type": 'group', "id": 1, "name": "my_group"}
        self.new_response.request.action = "del"
        self.manager.manage.return_value = [{"id": 1, "name": "my_group", "admin_id": 1}]
        self.new_response.request.account["id"] = 2

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("failed", taken_response.status)
        self.assertEqual("bad account id", taken_response.result["error"])

    def test_del_bad_group_id(self):
        self.new_response.request.object = {"type": 'group', "id": 1, "name": "my_group"}
        self.new_response.request.action = "del"
        self.manager.manage.return_value = []

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("failed", taken_response.status)
        self.assertEqual("bad group id", taken_response.result["error"])

    def test_del_no_id(self):
        self.new_response.request.object = {"type": 'group', "name": "my_group"}
        self.new_response.request.action = "del"

        taken_response = self.processor.process(self.new_response)

        self.assertEqual("failed", taken_response.status)
        self.assertEqual("no id", taken_response.result["error"])
        self.manager.manage.assert_not_called()
