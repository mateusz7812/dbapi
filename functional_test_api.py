from twisted.trial import unittest
from twisted.web.client import Agent, readBody
from twisted.internet import reactor
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer
from io import BytesIO
import json


class TestServer(unittest.TestCase):

    def setUp(self):
        self.api = Agent(reactor)

    def tearDown(self):
        self.api = None

    def test_procedure(self):
        # user is being registered
        received_answer, correct_answer = self.get_answers(['user', 'register', 'nick', 'login', 'password'], True)
        self.assertEqual(received_answer, correct_answer)

        # user is being logged in
        received_answer, _ = self.get_answers(['user', 'login', 'login', 'password'])
        unpacked_received = self.unpack_answer(received_answer)
        self.assertisnotEqual(unpacked_received, -1)

        user_key = unpacked_received

        # lists are being loaded
        received_answer, correct_answer = self.get_answers(['list', 'get', user_key], [])
        self.assertEqual(received_answer, correct_answer)

        # list is being added
        received_answer, _ = self.get_answers(['list', 'add', user_key, 'testowa', 'content'])
        unpacked_received = self.unpack_answer(received_answer)
        self.assertisnotEqual(unpacked_received, -1)

        list_id = unpacked_received

        # added list is being checked
        received_answer, correct_answer = self.get_answers(['list', 'get', user_key], [['testowa', 'content']])
        self.assertEqual(received_answer, correct_answer)

        # list is being deleted
        received_answer, correct_answer = self.get_answers(['list', 'del', user_key, list_id], True)
        self.assertEqual(received_answer, correct_answer)

        # lists are being loaded
        received_answer, correct_answer = self.get_answers(['list', 'get', user_key], [])
        self.assertEqual(received_answer, correct_answer)

        # user is being logged out
        received_answer, _ = self.get_answers(['user', 'logout', user_key])
        unpacked_received = self.unpack_answer(received_answer)
        self.assertisnotEqual(unpacked_received, -1)

        # list is being added, but it end bad
        received_answer, correct_answer = self.get_answers(['list', 'add', user_key, 'testowa', 'content'], -1)
        self.assertisEqual(received_answer, correct_answer)

    def make_response(self, body):
        return self.api.request(
            bytes('POST', 'utf8'),
            bytes('http://localhost:8080', 'utf8'),
            Headers({'User-Agent': ['Twisted Web Client Example']}),
            body)

    def readData(self, res):
        body = readBody(res)
        return body

    def unpack_answer(self, answer):
        unpacked_answer = json.loads(answer)
        return unpacked_answer

    def prepare_body(self, data: []):
        data = json.dumps(data)
        body = FileBodyProducer(BytesIO(bytes(data, "utf-8")))
        return body

    def prepare_correct_answer(self, data: []):
        answer = bytes(json.dumps(data), "utf-8")
        return answer

    def get_answers(self, request_data: [], correct_answer=None):
        body = self.prepare_body(request_data)
        correct_answer = self.prepare_correct_answer(correct_answer)

        response = self.make_response(body)
        received_answer = self.readData(response)

        return received_answer, correct_answer
