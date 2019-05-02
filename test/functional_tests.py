import json
from time import sleep
from unittest import TestCase

import requests

from DataWriter.TextWriter import TextWriter
from Main import Main
from RequestTaker.TwistedTaker import TwistedTaker
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from RequestsForwarder.BasicForwarder import BasicForwarder
from Responses.BasicResponseGenerator import BasicResponseGenerator
from TaskProcessor.AccountProcessor import AccountProcessor
from WriteManager.AccountsManager import AccountsManager


def get_response(data):
    data_dumped = json.dumps(data)
    response = requests.post("http://127.0.0.1:8080", data_dumped)
    return json.loads(response.content)


requestGenerator = BasicRequestGenerator
responseGenerator = BasicResponseGenerator
forwarder = BasicForwarder(responseGenerator)
account_processor = AccountProcessor(requestGenerator)
account_manager = AccountsManager()
text_writer = TextWriter("accounts")
account_manager.add_writer(text_writer)
account_processor.add_manager(account_manager)
forwarder.add_processor(account_processor)
taker = TwistedTaker(requestGenerator, forwarder)


class FunctionalTests(TestCase):
    def setUp(self):
        self.main = Main([taker])
        self.main.start()
        sleep(0.5)

    def tearDown(self):
        self.main.stop()

    def test_new_user_sequence(self):
        # account add
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login', "password": 'password', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # account get
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login', "password": 'password'},
             "action": 'get'})
        account = response["objects"][0]
        self.assertEqual("handled", response["status"])
        self.assertEqual("login", account["login"])
        self.assertEqual("password", account["password"])
        self.assertEqual("nick", account["nick"])
        self.assertEqual(int, type(account["id"]))

        # account delete
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login', "password": 'password'},
             "action": 'del'})
        account = response["objects"][0]
        self.assertEqual("handled", response["status"])
        self.assertEqual("login", account["login"])
        self.assertEqual("password", account["password"])
        self.assertEqual("nick", account["nick"])
        self.assertEqual(int, type(account["id"]))

    def test_two_same_users_sequence(self):
        # account add
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login', "password": 'password', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # same login account add
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login', "password": 'other', "nick": 'other'},
             "action": 'add'})
        self.assertEqual("failed", response["status"])

        # same nick account add
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'other', "password": 'other', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("failed", response["status"])

        # account get
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login', "password": 'password'},
             "action": 'get'})
        account = response["objects"][0]
        self.assertEqual("handled", response["status"])
        self.assertEqual("login", account["login"])
        self.assertEqual("password", account["password"])
        self.assertEqual("nick", account["nick"])
        self.assertEqual(int, type(account["id"]))

        # account delete
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login', "password": 'password'},
             "action": 'del'})
        account = response["objects"][0]
        self.assertEqual("handled", response["status"])
        self.assertEqual("login", account["login"])
        self.assertEqual("password", account["password"])
        self.assertEqual("nick", account["nick"])
        self.assertEqual(int, type(account["id"]))

    def test_more_new_users_sequence(self):
        # accounts add
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login1', "password": 'password', "nick": 'nick1'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login2', "password": 'password', "nick": 'nick2'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login3', "password": 'password', "nick": 'nick3'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # accounts get
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login1', "password": 'password'},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual("nick1", response["objects"][0]["nick"])

        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login2', "password": 'password'},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual("nick2", response["objects"][0]["nick"])
        response = get_response(

            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login3', "password": 'password'},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual("nick3", response["objects"][0]["nick"])

        # account delete
        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login1', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login2', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {"type": "anonymous"},
             "object": {"type": 'account', "login": 'login3', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

