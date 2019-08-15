from unittest import TestCase
from unittest.mock import Mock

from Processors.SessionProcessor import SessionProcessor
from Requests.Request import Request
from Requests.RequestGenerator import RequestGeneratorInterface
from Responses.Response import Response

processor = SessionProcessor
requestsGenerator = RequestGeneratorInterface


def retval(action, val):
    if action == "add":
        return True
    return []


class TestSessionProcessor(TestCase):
    def setUp(self):
        self.processor = processor(requestsGenerator)

        self.manager = Mock()
        self.manager.name = "session"
        self.processor.manager = self.manager

        self.response = Response("", Request({}, {"type": "session", "user_id": 1}, ""))

    def test_settings(self):
        self.assertEqual("session", self.processor.name)

    def test_add(self):
        self.response.request.action = "add"
        self.manager.manage.side_effect = retval

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)

    def test_generate_unique_key(self):
        self.response.request.action = "add"

        generated_keys = 0

        def manage(action, data):
            if action == "get":
                if "key" in data.keys():
                    nonlocal generated_keys
                    if generated_keys:
                        return []
                    generated_keys += 1
                    return [{"user_id": 3, "key": "12342345"}]

        self.manager.manage.side_effect = manage

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)

    def test_get(self):
        self.response.request.action = "get"
        self.response.request.account = {"type": "session", "user_id": 1, "key": "1234567890123456789012345"}
        self.manager.manage.return_value = [{"user_id": 1, "key": "1234567890123456789012345"}]

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)
        self.manager.manage.assert_called_with('get', {"user_id": 1})
        self.assertEqual([{'key': '1234567890123456789012345', 'user_id': 1}],
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
