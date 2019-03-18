from unittest import TestCase
from unittest.mock import patch

from DBManager import UsersDBManager, ListsDBManager
from DataBaseExecutors import TextBExecutor
from Forwarder import TaskForwarder
from Processor import UsersProcessor, ListsProcessor
from SessionManager import SessionManager
from TempDataExecutors import TextTempExecutor


def retfunc(value):
    return value


class TestForwarder(TestCase):
    def setUp(self):
        dataWriter = TextBExecutor()
        usersDBM = UsersDBManager(dataWriter)
        listsDBM = ListsDBManager(dataWriter)
        sessionWriter = TextTempExecutor()
        sessionsM = SessionManager(sessionWriter)
        usersP = UsersProcessor(usersDBM, sessionsM)
        listsP = ListsProcessor(listsDBM, sessionsM)
        self.forwarder = TaskForwarder(usersP=usersP, listsP=listsP)

    @patch('Processor.UsersProcessor.register', side_effect=retfunc)
    def test_user_register(self, test_patch):
        test_patch.return_value = test_patch
        request = {"object": 'user', "action": 'reg',
                   "login": 'login', "password": 'password', "nick": 'nick'}
        result = self.forwarder.forward(request)
        self.assertEqual(result, {'login': 'login', 'nick': 'nick',
                                  'password': 'password'})

    @patch('Processor.UsersProcessor.login', side_effect=retfunc)
    def test_user_login(self, test_patch):
        test_patch.return_value = test_patch
        request = {"object": 'user', "action": 'login',
                   "login": 'login', "password": 'password'}
        result = self.forwarder.forward(request)
        self.assertEqual(result, {'login': 'login', 'password': 'password'})

    @patch('Processor.UsersProcessor.logout', side_effect=retfunc)
    def test_user_logout(self, test_patch):
        test_patch.return_value = test_patch
        request = {"object": 'user', "action": 'logout',
                   "user_id": "user_id", "user_key": "user_key"}
        result = self.forwarder.forward(request)
        self.assertEqual(result, {"user_id": "user_id", "user_key": "user_key"})

    @patch('Processor.UsersProcessor.delete', side_effect=retfunc)
    def test_user_delete(self, test_patch):
        test_patch.return_value = test_patch
        request = {"object": 'user', "action": 'delete',
                   "user_id": "user_id", "user_key": "user_key",
                   "login": 'login', "password": 'password'}
        result = self.forwarder.forward(request)
        self.assertEqual(result, {"user_id": "user_id", "user_key": "user_key",
                                  "login": 'login', "password": 'password'})

    @patch('Processor.ListsProcessor.add', side_effect=retfunc)
    def test_list_add(self, test_patch):
        test_patch.return_value = test_patch
        request = {"object": 'list', "action": 'add',
                   "user_id": "user_id", "user_key": "user_key",
                   "name": 'testowa', "content": 'content'}
        result = self.forwarder.forward(request)
        self.assertEqual(result, {"user_id": "user_id", "user_key": "user_key",
                                  "name": 'testowa', "content": 'content'})

    @patch('Processor.ListsProcessor.get', side_effect=retfunc)
    def test_list_get(self, test_patch):
        test_patch.return_value = test_patch
        request = {"object": 'list', "action": 'get',
                   "user_id": "user_id", "user_key": "user_key"}
        result = self.forwarder.forward(request)
        self.assertEqual(result, {"user_id": "user_id", "user_key": "user_key"})

    @patch('Processor.ListsProcessor.delete', side_effect=retfunc)
    def test_list_delete(self, test_patch):
        test_patch.return_value = test_patch
        request = {"object": 'list', "action": 'del',
                   "user_id": "user_id", "user_key": "user_key",
                   "list_id": "list_id"}
        result = self.forwarder.forward(request)
        self.assertEqual(result, {"user_id": "user_id", "user_key": "user_key",
                                  "list_id": "list_id"})





