import json
import requests
from twisted.internet import reactor
from twisted.trial._asynctest import TestCase
from twisted.web import server
from NetworkApi import NetApi, BaseHandler


def make_request(data: str, port: int):
    r = requests.post("http://localhost:{}".format(port), data=json.dumps(data))
    return r.content


class TestBranchHandler(BaseHandler):
    def process_request(self, data: str):
        return data


class TestAPI(TestCase):
    def setUp(self):
        site = server.Site(NetApi(TestBranchHandler))
        self.port = reactor.listenTCP(9000, site)

    def tearDown(self):
        self.port.stop()

    def test_aliveness(self):
        self.assertEqual(make_request("some data", 9000), "some data")



