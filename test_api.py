from twisted.trial import unittest
from twisted.web.client import Agent, readBody
from twisted.internet import reactor
from twisted.web.http_headers import Headers


class TestServer(unittest.TestCase):

    def setUp(self):
        self.api = Agent(reactor)

    def tearDown(self):
        self.api = None

    def test_hello(self):
        response = self.api.request(
            bytes('GET', 'utf8'),
            bytes('http://localhost:8080', 'utf8'),
            Headers({'User-Agent': ['Twisted Web Client Example']}),
            None)

        def readData(res):
            body = readBody(res)
            return body

        response.addCallback(readData)
        response.addCallback(lambda x: self.assertEqual(x, b"Hello, world!"))
        return response


