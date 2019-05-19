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
        time.sleep(0.1)

    def tearDown(self):
        self.program.stop()

    def test_taking(self):
        data = {
            "account": {"type": "anonymous"},
            "object": "user",
            "action": "add",
            "data": {
                "login": "test",
                "password": "test"
            }
        }

        data_dumped = json.dumps(data)
        all_requests = taker.requests_writer.select({})
        if len(all_requests):
            id = int(max([x["id"] for x in all_requests])) + 1
        else:
            id = 1
        taker.requests_writer.insert({"id": id, "request": data_dumped})

        time.sleep(2)

        response_dumped = taker.responses_writer.select({"id": id})[0]["response"]

        response_data = json.loads(response_dumped)
        self.assertEqual(data, response_data)
