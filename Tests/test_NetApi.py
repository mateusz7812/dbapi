from multiprocessing import Process
from unittest import TestCase

from WriteManager.DBManager import UsersDBManager, ListsDBManager
from Tests.functions_for_tests import get_response
from DataWriter.DataBaseExecutors import TextBExecutor
from ObjectForwarder.Forwarder import TaskForwarder
from RequestTaker.Http import HttpApi
from TaskProcessor.Processor import UsersProcessor, ListsProcessor
from WriteManager.SessionManager import SessionManager
from DataWriter.TempDataExecutors import TextTempExecutor

test_running = 0


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
        self.server = Process(target=httpApi.run)
        self.server.start()

    def tearDown(self):
        self.server.terminate()
        self.server.join()

    def test_post(self):
        print("1")
        response: {} = get_response({"object": "invalid"})
        self.assertEqual("object not found", response["info"])

