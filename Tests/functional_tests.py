import json
from time import sleep
from unittest import TestCase

import requests

from Main import Main
from RequestsForwarder.ForwarderInterface import Forwarder
from RequestTaker.TwistedTaker import TwistedTaker
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Responses.ResponseGeneratorInterface import ResponseGenerator


def get_response(data):
    data_dumped = json.dumps(data)
    response = requests.post("http://127.0.0.1:8080", data_dumped)
    return json.loads(response.content)


forwarder = Forwarder()
requestGenerator = BasicRequestGenerator()
responseGenerator = ResponseGenerator([forwarder])
taker = TwistedTaker(requestGenerator, responseGenerator)


class FunctionalTests(TestCase):
    def setUp(self):
        self.main = Main([taker])
        self.main.start()
        sleep(0.5)

    def tearDown(self):
        self.main.stop()

    def test_new_user_sequence(self):
        # user is being registered
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'user', "login": 'login', "password": 'password', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("user added", response["info"])

        # user is being logged in
        response = get_response(
            {"account": {"login": 'login', "password": 'password'},
             "object": {"type": 'session'},
             "action": 'add', })
        self.assertEqual("session added", response["info"])
        self.assertEqual(int, type(response["user_id"]))
        self.assertEqual(str, type(response["user_key"]))
        user_id = response["user_id"]
        user_key = response["user_key"]
