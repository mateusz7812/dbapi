import json
import os
from time import sleep
from unittest import TestCase

import requests

from Writers.TextWriter import TextWriter
from Main import Main
from Takers.TwistedTaker import TwistedTaker
from Requests.RequestGeneratorBasic import BasicRequestGenerator
from Forwarders.BasicForwarder import BasicForwarder
from Responses.BasicResponseGenerator import BasicResponseGenerator
from Processors.AccountProcessor import AccountProcessor
from Processors.ListProcessor import ListProcessor
from Managers.AccountsManager import AccountsManager
from Managers.ListsManager import ListsManager
from Managers.ManagerInterface import Manager


def get_response(data):
    data_dumped = json.dumps(data)
    response = requests.post("http://127.0.0.1:8080", data_dumped)
    return json.loads(response.content)


requestGenerator = BasicRequestGenerator
responseGenerator = BasicResponseGenerator
forwarder = BasicForwarder(responseGenerator)

account_processor = AccountProcessor(requestGenerator)
account_manager = AccountsManager()
accounts_writer = TextWriter("accounts")
account_manager.add_writer(accounts_writer)
account_processor.add_manager(account_manager)
forwarder.add_processor(account_processor)

list_processor = ListProcessor(requestGenerator)
lists_manager = ListsManager()
lists_writer = TextWriter("lists")
lists_manager.add_writer(lists_writer)
list_processor.add_manager(lists_manager)
forwarder.add_processor(list_processor)

taker = TwistedTaker(requestGenerator, forwarder)


class FunctionalTests(TestCase):
    def setUp(self):
        self.main = Main([taker])
        self.main.start()
        lists_writer.delete({})
        accounts_writer.delete({})
        sleep(0.5)

    def tearDown(self):
        self.main.stop()

    def test_new_list_sequence(self):
        # account add
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login', "password": 'password', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # list add
        response = get_response(
            {"account": {"login": 'login', "password": 'password'},
             "object": {"type": 'list', "name": "name",
                        "content": json.dumps(["buy milk", "drink milk", "throw away box"])},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # list get
        response = get_response(
            {"account": {"login": 'login', "password": 'password'},
             "object": {"type": 'list', "name": "name"},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual(1, len(response["objects"]))
        list_object = response["objects"][0]
        self.assertEqual(["buy milk", "drink milk", "throw away box"], json.loads(list_object["content"]))

        # list del
        response = get_response(
            {"account": {"login": 'login', "password": 'password'},
             "object": {"type": 'list', "name": "name"},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

        # list get
        response = get_response(
            {"account": {"login": 'login', "password": 'password'},
             "object": {"type": 'list', "name": "name"},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual(0, len(response["objects"]))

        # account delete
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

    def test_new_user_sequence(self):
        # account add
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login', "password": 'password', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # account get
        response = get_response(
            {"account": {},
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
            {"account": {},
             "object": {"type": 'account', "login": 'login', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])
        account = response["objects"][0]
        self.assertEqual("handled", response["status"])
        self.assertEqual("login", account["login"])
        self.assertEqual("password", account["password"])
        self.assertEqual("nick", account["nick"])
        self.assertEqual(int, type(account["id"]))

    def test_two_same_users_sequence(self):
        # account add
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login', "password": 'password', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # same login account add
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login', "password": 'other', "nick": 'other'},
             "action": 'add'})
        self.assertEqual("failed", response["status"])
        self.assertEqual("taken login", response["error"])

        # same nick account add
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'other', "password": 'other', "nick": 'nick'},
             "action": 'add'})
        self.assertEqual("failed", response["status"])
        self.assertEqual("taken nick", response["error"])

        # account get
        response = get_response(
            {"account": {},
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
            {"account": {},
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
            {"account": {},
             "object": {"type": 'account', "login": 'login1', "password": 'password', "nick": 'nick1'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login2', "password": 'password', "nick": 'nick2'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login3', "password": 'password', "nick": 'nick3'},
             "action": 'add'})
        self.assertEqual("handled", response["status"])

        # accounts get
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login1', "password": 'password'},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual("nick1", response["objects"][0]["nick"])

        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login2', "password": 'password'},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual("nick2", response["objects"][0]["nick"])
        response = get_response(

            {"account": {},
             "object": {"type": 'account', "login": 'login3', "password": 'password'},
             "action": 'get'})
        self.assertEqual("handled", response["status"])
        self.assertEqual("nick3", response["objects"][0]["nick"])

        # account delete
        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login1', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login2', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

        response = get_response(
            {"account": {},
             "object": {"type": 'account', "login": 'login3', "password": 'password'},
             "action": 'del'})
        self.assertEqual("handled", response["status"])

