import json

from twisted.internet.protocol import Factory
from twisted.test import proto_helpers
from twisted.trial._asynctest import TestCase
from twisted.web import server

from HttpApi import HttpApi, BaseHandler


class TestBranchHandler(BaseHandler):
    def process_request(self, data: str):
        return data


class TestAPI(TestCase):
    def setUp(self):
        site = server.Site(HttpApi(TestBranchHandler))
        self.proto = site.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def _test(self, operation, expected):
        self.tr.write(bytes("data", "utf-8"))
        self.assertEqual(self.tr.value(), expected)

    def test_aliveness(self):
        self._test(bytes("data", "utf-8"), "some data")



