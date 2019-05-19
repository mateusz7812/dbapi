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
        self.assertEqual(self.guard.authorization_methods, ["session", "account", "admin"])
        self.assertTrue(issubclass(guard, Guard))

    def test_internal_security(self):
        self.response.request.account["type"] = "internal"

        result = self.guard.resolve(self.response)

        self.assertFalse(result)

    def test_account_authorization(self):
        self.response.request.account = {"type": "account", "login": "login", "password": "password"}
        processor = Mock()
        processor.process.return_value = [{"id": 1, "login": "login", "password": "password"}]
        self.guard.processors["account"] = processor

        result = self.guard.resolve(self.response)

        self.assertEqual(processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': 'login'})
        self.assertTrue(result)

    def test_account_authorization_bad_pass(self):
        self.response.request.account = {"type": "account", "login": "login", "password": "wrong"}
        processor = Mock()
        processor.process.return_value = [{"id": 1, "login": "login", "password": "password"}]
        self.guard.processors["account"] = processor

        result = self.guard.resolve(self.response)

        self.assertEqual(self.guard.processors["account"].process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': 'login'})
        self.assertFalse(result)

    def test_session_authorization(self):
        self.response.request.account = {"type": "session", "user_id": 1, "key": "123345245245423543"}
        processor = Mock()
        processor.process.return_value = [{"user_id": 1, "key": "123345245245423543"}, {"user_id": 1, "key": "1233"}]
        self.guard.processors["session"] = processor

        result = self.guard.resolve(self.response)

        self.assertEqual(processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'session', 'user_id': 1})
        self.assertTrue(result)

    def test_session_authorization_bad_pass(self):
        self.response.request.account = {"type": "session", "user_id": 1, "key": "wrong"}
        processor = Mock()
        processor.process.return_value = [{"user_id": 1, "key": "123345245245423543"}, {"user_id": 1, "key": "1233"}]
        self.guard.processors["session"] = processor

        result = self.guard.resolve(self.response)

        self.assertEqual(processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'session', 'user_id': 1})
        self.assertFalse(result)

    def test_admin_authorization(self):
        self.response.request.account = {"type": "admin", "login": "login", "password": "password"}

        account_processor = Mock()
        account_processor.process.return_value = [{"id": 1, "login": "login", "password": "password"}]
        self.guard.processors["account"] = account_processor

        admin_processor = Mock()
        admin_processor.process.return_value = [{"id": 3, "user_id": 1}]
        self.guard.processors["admin"] = admin_processor

        result = self.guard.resolve(self.response)

        self.assertEqual(account_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': "login"})
        self.assertEqual(admin_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'admin', 'user_id': 1})
        self.assertTrue(result)

    def test_admin_authorization_bad_pass(self):
        self.response.request.account = {"type": "admin", "login": "login", "password": "wrong"}

        account_processor = Mock()
        account_processor.process.return_value = [{"id": 1, "login": "login", "password": "password"}]
        self.guard.processors["account"] = account_processor

        admin_processor = Mock()
        admin_processor.process.return_value = [{"id": 3, "user_id": 1}]
        self.guard.processors["admin"] = admin_processor

        result = self.guard.resolve(self.response)

        self.assertEqual(account_processor.process.call_args_list[0][0][0].request.object,
                         {'type': 'account', 'login': "login"})

        self.assertEqual(admin_processor.process.call_args_list,
                         [])
        self.assertFalse(result)
