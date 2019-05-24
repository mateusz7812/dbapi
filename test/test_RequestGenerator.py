import copy
from unittest import TestCase

from Requests.Request import Request
from Requests.RequestGenerator import RequestGenerator

requestGenerator = RequestGenerator


class TestRequestGenerator(TestCase):
    def setUp(self):
        self.generator = requestGenerator()

    def test_request(self):
        request = Request({"type": "anonymous"}, {"type": "account", "login": "test", "password": "test"}, "add")

        self.assertEqual(request.account, {"type": "anonymous"})
        self.assertEqual(request.object, {"type": "account", "login": "test", "password": "test"})
        self.assertEqual(request.action, "add")

    def test_generate(self):
        request: Request = self.generator.generate(
            {"account": {"type": "anonymous"}, "object": {"type": "account", "login": "test", "password": "test"},
             "action": "add"})

        expected_request = Request({"type": "anonymous"}, {"type": "account", "login": "test", "password": "test"},
                                        "add")

        self.assertEqual(expected_request.account, request.account)
        self.assertEqual(expected_request.object, request.object)
        self.assertEqual(expected_request.action, request.action)
