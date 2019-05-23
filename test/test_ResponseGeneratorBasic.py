from unittest import TestCase

from Requests.BasicRequest import BasicRequest
from Responses.BasicResponse import BasicResponse
from Responses.BasicResponseGenerator import BasicResponseGenerator

generator = BasicResponseGenerator


class TestBasicResponseGenerator(TestCase):
    def setUp(self):
        self.generator = generator()

        self.request = BasicRequest({"type": "anonymous"}, {"type": "account", "login": "test", "password": "test"}, "add")

    def test_response(self):
        response = BasicResponse("new", self.request)

        self.assertEqual("new", response.status)
        self.assertEqual(self.request, response.request)
        self.assertEqual({}, response.result)

    def test_generate(self):
        response = self.generator.generate(self.request)

        self.assertEqual("new", response.status)
        self.assertEqual(self.request, response.request)
        self.assertEqual({}, response.result)
