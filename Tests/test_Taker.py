import json
from unittest import TestCase
from unittest.mock import patch

import requests

from Main import Main
from ObjectForwarder.ForwarderInterface import Forwarder
from RequestTaker.TwistedTaker import TwistedTaker

taker = TwistedTaker
forwarder = Forwarder


def retfunc(value):
    return value


class TestTaker(TestCase):
    def setUp(self):
        self.program = Main([forwarder], [taker])
        self.program.start()

    def tearDown(self):
        self.program.stop()

    def test_alive(self):
        response = requests.get("http://127.0.0.1:8080")
        self.assertEqual(200, response.status_code)

    @patch('RequestTaker.TwistedTaker.TwistedTaker.take', side_effect=retfunc)
    def test_taking(self, test_patch):
        data = {
            "user": None,
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
