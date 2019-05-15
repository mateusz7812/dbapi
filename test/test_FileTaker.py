import json
import os
import time
from unittest import TestCase

from Forwarders.ForwarderInterface import Forwarder
from Main import Main
from Requests.RequestGeneratorInterface import RequestGenerator
from Responses.ResponseGeneratorInterface import ResponseGenerator
from Takers.FileTaker import FileTaker


class MockFileTaker(FileTaker):
    def take(self, data):
        return data


responseGenerator = ResponseGenerator
forwarder = Forwarder(responseGenerator)
requestGenerator = RequestGenerator
taker = MockFileTaker(requestGenerator, forwarder)


class TestTaker(TestCase):
    def setUp(self):
        self.program = Main([taker])
        self.program.start()
        time.sleep(0.5)

    def tearDown(self):
        self.program.stop()

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
        data_to_save = "1;"+data_dumped+"\n"

        with open("data/requests", "w") as f:
            f.write(data_to_save)

        time.sleep(2)

        with open("data/responses") as f:
            read_data = [x[:-1] for x in f.readlines()]

        response_dumped = json.dumps("lack of data")
        for x in read_data:
            separated = x.split(";")
            if separated[0] == "1":
                response_dumped = separated[1]
                break

        response_data = json.loads(response_dumped)
        self.assertEqual(data, response_data)
