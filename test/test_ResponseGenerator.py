from unittest import TestCase

from Requests.Request import Request
from Responses.Response import Response
from Responses.ResponseGenerator import ResponseGenerator

generator = ResponseGenerator


class TestResponseGenerator(TestCase):
    def setUp(self):
        self.generator = generator()

        self.request = Request({"type": "anonymous"}, {"type": "account", "login": "test", "password": "test"}, "add")

    def test_response(self):
        response = Response("new", self.request)

        self.assertEqual("new", response.status)
        self.assertEqual(self.request, response.request)
        self.assertEqual({}, response.result)

    def test_generate(self):
        response = self.generator.generate(self.request)

        self.assertEqual("new", response.status)
        self.assertEqual(self.request, response.request)
        self.assertEqual({}, response.result)
