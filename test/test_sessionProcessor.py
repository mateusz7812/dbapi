from unittest import TestCase
from unittest.mock import Mock

from Processors.SessionProcessor import SessionProcessor
from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Responses.BasicResponse import BasicResponse

processor = SessionProcessor
requestsGenerator = BasicRequestGenerator


def retval(action, val):
    if action == "add":
        return True
    return []


class TestSessionProcessor(TestCase):
    def setUp(self):
        self.processor = processor(requestsGenerator)

        self.manager = Mock()
        self.manager.name = "session"
        self.manager.manage.return_value = True
        self.processor.add_manager(self.manager)

        self.response = BasicResponse("new",
                                      BasicRequest({"login": "test", "password": "test"},
                                                   {"type": "session"},
                                                   "add"))

        self.response.request.required["account"] = {"objects": [{"id": 1, "login": "test", "password": "test"}]}

    def test_settings(self):
        self.assertEqual("session", self.processor.name)
        self.assertEqual(1, len(self.processor.managers))
        self.assertEqual(requestsGenerator, type(self.processor.request_generator))

    def test_required_requests_for_add(self):
        required_requests = self.processor.get_required_requests(self.response)

        self.assertEqual(1, len(required_requests))
        self.assertIsInstance(required_requests[0], BasicRequest)
        self.assertEqual("test", required_requests[0].object["login"])
        self.assertEqual("test", required_requests[0].object["password"])

    def test_required_requests_for_get(self):
        self.response.request.action = "get"
        self.response.request.account = {"type": "session", "user_id": 1, "key": "21431231231"}

        required_requests = self.processor.get_required_requests(self.response)

        self.assertEqual(1, len(required_requests))
        self.assertIsInstance(required_requests[0], BasicRequest)
        self.assertEqual(1, required_requests[0].object["id"])

    def test_add(self):
        self.manager.manage = retval

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)
        self.assertEqual(str, type(taken_response.result["objects"][0]["key"]))
        self.assertEqual(25, len(taken_response.result["objects"][0]["key"]))
        self.assertEqual(1, taken_response.result["objects"][0]["user_id"])

    def test_get_user(self):
        self.response.request.action = "get"
        self.response.request.account = {"type": "session", "user_id": 1, "key": "1234567890123456789012345"}
        self.manager.manage.return_value = [{"user_id": 1, "key": "1234567890123456789012345"}]

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('get', {"user_id": 1})
        self.assertEqual([{"id": 1, "login": "test", "password": "test"}],
                         taken_response.result["objects"])

    def test_del(self):
        self.response.request.action = "del"
        self.response.request.object["user_id"] = 1
        self.manager.manage.return_value = [{"user_id": 1, "key": "1234567890123456789012345"}]

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('del', {"user_id": 1})
        self.assertIn({"user_id": 1, "key": "1234567890123456789012345"},
                      taken_response.result["objects"])
