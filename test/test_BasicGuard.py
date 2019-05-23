from unittest import TestCase
from unittest.mock import Mock

from Guards.BasicGuard import BasicGuard
from Guards.GuardInterface import Guard
from Requests.BasicRequest import BasicRequest
from Responses.BasicResponse import BasicResponse

guard = BasicGuard


class TestBasicGuard(TestCase):
    def setUp(self):
        self.guard = guard()

        self.response = BasicResponse("new", BasicRequest({}, {}, ""))

    def test_settings(self):
        self.assertEqual(self.guard.authorization_methods, ["anonymous", "session", "account", "admin"])
        self.assertTrue(issubclass(guard, Guard))

    def test_account_authorization(self):
        self.response.request.account = {"type": "account", "login": "login", "password": "password"}
        self.response.request.object = {"type": "test"}
        self.response.request.action = "test"

        test_processor = Mock()
        test_processor.name = "test"
        test_processor.authorization_rules = {"test": {"account": [set()]}}
        self.guard.processors["test"] = test_processor

        account_processor = Mock()
        account_processor.process.return_value = Mock()
        account_processor.process.return_value.result = {
            "objects": [{"id": 1, "login": "login", "password": "password"}]}
        self.guard.processors["account"] = account_processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(account_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': 'login'})
        self.assertEqual(resolved_response.status, "authorized")

    def test_account_authorization_bad_pass(self):
        self.response.request.account = {"type": "account", "login": "login", "password": "wrong"}
        processor = Mock()
        processor.process.return_value = Mock()
        processor.process.return_value.result = {"objects": [{"id": 1, "login": "login", "password": "password"}]}
        self.guard.processors["account"] = processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(self.guard.processors["account"].process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': 'login'})
        self.assertEqual(resolved_response.status, "not authorized")

    def test_session_authorization(self):
        self.response.request.account = {"type": "session", "user_id": 1, "key": "123345245245423543"}
        self.response.request.object = {"type": "test"}
        self.response.request.action = "test"

        account_processor = Mock()
        account_processor.process.return_value = Mock()
        account_processor.process.return_value.result = {"objects": [{"id": 1, "login": "login", "password": "password"}]}
        self.guard.processors["account"] = account_processor

        test_processor = Mock()
        test_processor.name = "test"
        test_processor.authorization_rules = {"test": {"session": [set()]}}
        self.guard.processors["test"] = test_processor

        session_processor = Mock()
        session_processor.process.return_value = Mock()
        session_processor.process.return_value.result = {
            "objects": [{"user_id": 1, "key": "123345245245423543"}, {"user_id": 1, "key": "1233"}]}
        self.guard.processors["session"] = session_processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(session_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'session', 'user_id': 1})
        self.assertEqual(resolved_response.status, "authorized")

    def test_session_authorization_bad_pass(self):
        self.response.request.account = {"type": "session", "user_id": 1, "key": "wrong"}
        session_processor = Mock()
        session_processor.process.return_value = Mock()
        session_processor.process.return_value.result = {
            "objects": [{"user_id": 1, "key": "123345245245423543"}, {"user_id": 1, "key": "1233"}]}
        self.guard.processors["session"] = session_processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(session_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'session', 'user_id': 1})
        self.assertEqual(resolved_response.status, "not authorized")

    def test_admin_authorization(self):
        self.response.request.account = {"type": "admin", "login": "login", "password": "password"}
        self.response.request.object = {"type": "test"}
        self.response.request.action = "test"

        test_processor = Mock()
        test_processor.name = "test"
        test_processor.authorization_rules = {"test": {"admin": [set()]}}
        self.guard.processors["test"] = test_processor

        account_processor = Mock()
        account_processor.process.return_value = Mock()
        account_processor.process.return_value.result = {
            "objects": [{"id": 1, "login": "login", "password": "password", "account_type": "admin"}]}
        self.guard.processors["account"] = account_processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(account_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': "login"})
        self.assertEqual(resolved_response.status, "authorized")

    def test_admin_authorization_bad_pass(self):
        self.response.request.account = {"type": "admin", "login": "login", "password": "wrong"}

        account_processor = Mock()
        account_processor.process.return_value = Mock()
        account_processor.process.return_value.result = {
            "objects": [{"id": 1, "login": "login", "password": "password", "account_type": "admin"}]}
        self.guard.processors["account"] = account_processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(account_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': "login"})

        self.assertEqual(resolved_response.status, "not authorized")

    def test_add_user_authorization(self):
        self.response.request.account = {"type": "anonymous"}
        self.response.request.object = {"type": "account", "login": "login", "password": "password"}
        self.response.request.action = "add"

        account_processor = Mock()
        account_processor.authorization_rules = {
            "add": {"anonymous": [{"login", "password"}], "account": [], "session": [], "admin": [{}]}}
        self.guard.processors["account"] = account_processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(resolved_response.request.account, {"type": "anonymous"})

    def test_list_delete_authorization(self):
        self.response.request.account = {"type": "anonymous"}
        self.response.request.object = {"type": "list", "name": "name", "content": 'asdsadas'}
        self.response.request.action = "del"

        list_processor = Mock()
        list_processor.authorization_rules = {
            "del": {"anonymous": [], "account": [], "session": [], "admin": [{}]}}
        self.guard.processors["list"] = list_processor

        resolved_response = self.guard.resolve(self.response)

        self.assertEqual(resolved_response.status, "not authorized")

    def test_get_account(self):
        self.response.request.account = {"type": "account", "login": "login", "password": "password"}

        account_processor = Mock()
        account_processor.process.return_value = Mock()
        account_processor.process.return_value.result = {
            "objects": [{"id": 1, "login": "login", "password": "password"}]}
        self.guard.processors["account"] = account_processor

        request = self.guard.get_account(self.response.request)

        self.assertEqual(account_processor.process.call_args_list[0][0][0].request.object,
                         {"type": "account", "login": "login", "password": "password"})

        self.assertEqual(request.account, {"id": 1, "login": "login", "password": "password"})

    def test_get_account_by_session(self):
        self.response.request.account = {"type": "session", "user_id": 1, "key": "sdadsadadasd"}

        account_processor = Mock()
        account_processor.process.return_value = Mock()
        account_processor.process.return_value.result = {
            "objects": [{"id": 1, "login": "login", "password": "password"}]}
        self.guard.processors["account"] = account_processor

        request = self.guard.get_account(self.response.request)

        self.assertEqual(account_processor.process.call_args_list[0][0][0].request.object,
                         {"type": "account", "id": 1})

        self.assertEqual(request.account, {"id": 1, "login": "login", "password": "password"})
