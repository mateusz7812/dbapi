import json
import threading


import requests
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.trial._asynctest import TestCase
from twisted.web import server

from DBManager import UsersDBManager, ListsDBManager
from DataBaseExecutors import TextBExecutor
from Forwarder import TaskForwarder
from HttpApi import HttpApi
from Processor import UsersProcessor, ListsProcessor
from SessionManager import SessionManager
from TempDataExecutors import TextTempExecutor


class TestAPI(TestCase):
    def setUp(self):
        dataWriter = TextBExecutor()
        usersDBM = UsersDBManager(dataWriter)
        listsDBM = ListsDBManager(dataWriter)

        sessionWriter = TextTempExecutor()
        sessionsM = SessionManager(sessionWriter)

        usersP = UsersProcessor(usersDBM, sessionsM)
        listsP = ListsProcessor(listsDBM, sessionsM)

        forwarder = TaskForwarder(usersP=usersP, listsP=listsP)

        httpApi = HttpApi(forwarder)
        self.site = server.Site(httpApi)
        self.ltcp = reactor.listenTCP(8080, self.site)

    def tearDown(self):
        self.ltcp.stopListening()

    def make_request(self, data):
        r = requests.post("http://127.0.0.1:8080", data=json.dumps(data))
        return str(r.content, "utf-8")

    def test_post(self):
        print("1")

        d = Deferred()
        d.addCallback(lambda: self.make_request({"object": None}))
        d.addCallback(lambda response: self.assertEqual("object not found", response["info"]))
        return d
