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

    def test_register_user(self):
        data = json.dumps(['user', 'register', 'nick', 'login', 'password'])
        ret = bytes(json.dumps(True), "utf-8")
        body = FileBodyProducer(BytesIO(bytes(data, "utf-8")))

        response = self.make_response(body)
        response.addCallback(readData)

        response.addCallback(lambda x: self.assertEqual(x, ret))
        return response

    def test_login_user(self):
        data = json.dumps(['user', 'login', 'login', 'password'])
        ret = bytes(json.dumps(True), "utf-8")
        body = FileBodyProducer(BytesIO(bytes(data, "utf-8")))

        response = self.make_response(body)
        response.addCallback(readData)

        response.addCallback(lambda x: self.assertEqual(x, ret))
        return response

    def test_list(self):
        data = json.dumps(['list', 'add', 'name', 'content'])
        ret = bytes(json.dumps(True), "utf-8")
        body = FileBodyProducer(BytesIO(bytes(data, "utf-8")))

        response = self.make_response(body)
        response.addCallback(readData)

        response.addCallback(lambda x: self.assertEqual(x, ret))
        return response

    def make_response(self, body):
        return self.api.request(
            bytes('POST', 'utf8'),
            bytes('http://localhost:8080', 'utf8'),
            Headers({'User-Agent': ['Twisted Web Client Example']}),
            body)


def readData(res):
    body = readBody(res)
    return body
