import json
import time
from unittest import TestCase
from unittest.mock import patch, MagicMock

import requests

from Main import Main
from RequestsForwarder.ForwarderInterface import Forwarder
from RequestTaker.TwistedTaker import TwistedTaker
from Requests.RequestGeneratorInterface import RequestGenerator
from Responses.ResponseGeneratorInterface import ResponseGenerator


class MockTwistedTaker(TwistedTaker):
    def take(self, data):
        return data


forawrder = Forwarder()
requestGenerator = RequestGenerator()
responseGenerator = ResponseGenerator([forawrder])
taker = MockTwistedTaker(requestGenerator, responseGenerator)


class TestTaker(TestCase):
    def setUp(self):
        self.program = Main([taker])
        self.program.start()
        time.sleep(0.5)

    def tearDown(self):
        self.program.stop()

    def test_alive(self):
        response = requests.get("http://127.0.0.1:8080")
        self.assertEqual(200, response.status_code)

    def test_taking(self):
        data = {
            "account": None,
            "object": "user",
            "action": "add",
            "data": {
                "login": "test",
                "password": "test"
            }
        }
        data_dumped = json.dumps(data)
        response = requests.post("http://127.0.0.1:8080", data_dumped)
        response_data = json.loads(response.content)
        self.assertEqual(data, response_data)
