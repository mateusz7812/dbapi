import json
from unittest import TestCase
from unittest.mock import Mock

from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Responses.BasicResponse import BasicResponse
from TaskProcessor.ListProcessor import ListProcessor

processor = ListProcessor
requestsGenerator = BasicRequestGenerator


class TestListProcessor(TestCase):
    def setUp(self):
        self.processor = processor(requestsGenerator)

        self.manager = Mock()
        self.manager.name = "list"
        self.manager.manage.return_value = []
        self.processor.add_manager(self.manager)

        self.response = BasicResponse("new",
                                      BasicRequest({"login": "test", "password": "test"},
                                                   {"type": 'list', "name": "name", "content": json.dumps(
                                                       ["buy milk", "drink milk", "throw away box"])},
                                                   "add"))

    def test_Processor(self):
        self.assertEqual("list", self.processor.name)
        self.assertEqual(1, len(self.processor.managers))
        self.assertEqual(requestsGenerator, type(self.processor.request_generator))

    def test_required_requests(self):
        required_requests = self.processor.get_required_requests(self.response)
        self.assertEqual(1, len(required_requests))
        self.assertIsInstance(required_requests[0], BasicRequest)
        self.assertEqual("test", required_requests[0].object["login"])
        self.assertEqual("test", required_requests[0].object["password"])

    def test_add(self):
        self.response.request.required["account"] = [{"id": 1, "login": "test", "password": "test"}]
        taken_response = self.processor.process(self.response)
        self.assertEqual("handled", taken_response.status)
        print(self.manager.mock_calls)
        self.assertEqual(('add', {"id": 1, "user_id": 1, "name": "name", "content": json.dumps(["buy milk", "drink milk", "throw away box"])}), self.manager.manage.call_args[0])
