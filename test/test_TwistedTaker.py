import json
import time
from unittest import TestCase

import requests

from Main import Main
from Forwarders.ForwarderInterface import Forwarder
from Takers.TwistedTaker import TwistedTaker
from Requests.RequestGeneratorInterface import RequestGeneratorInterface
from Responses.ResponseGeneratorInterface import ResponseGeneratorInterface


class MockTwistedTaker(TwistedTaker):
    def take(self, data):
        return data


responseGenerator = ResponseGeneratorInterface
forwarder = Forwarder(responseGenerator)
requestGenerator = RequestGeneratorInterface
taker = MockTwistedTaker(requestGenerator, forwarder)


class TestTaker(TestCase):
    def setUp(self):
        self.program = Main([taker])
        self.program.start()
        time.sleep(0.5)

    def tearDown(self):
        self.program.stop()

    def test_alive(self):
        response = requests.get("http://127.0.0.1:7000")
        self.assertEqual(200, response.status_code)

    def test_taking(self):
        data = {
            "account": None,
            "object": {
                "login": "test",
                "password": "test"
            },
            "action": "add"
        }
        data_dumped = json.dumps(data)
        response = requests.post("http://127.0.0.1:7000", data_dumped)
        response_data = json.loads(response.content)
        self.assertEqual(data, response_data)
