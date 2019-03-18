from unittest import TestCase

from DBManager import UsersDBManager, ListsDBManager
from DataBaseExecutors import TextBExecutor
from Forwarder import TaskForwarder
from Processor import UsersProcessor, ListsProcessor
from SessionManager import SessionManager
from TempDataExecutors import TextTempExecutor


class TestForwarder(TestCase):
    def setUp(self):
        dataWriter = TextBExecutor()
        usersDBM = UsersDBManager(dataWriter)
        listsDBM = ListsDBManager(dataWriter)
        sessionWriter = TextTempExecutor()
        sessionsM = SessionManager(sessionWriter)
        usersP = UsersProcessor(usersDBM, sessionsM)
        listsP = ListsProcessor(listsDBM, sessionsM)
        processors = [usersP, listsP]
        self.forwarder = TaskForwarder(processors)

    def 




