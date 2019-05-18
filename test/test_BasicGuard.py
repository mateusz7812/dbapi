from unittest import TestCase

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
        self.assertEqual(self.guard.authorization_methods, ["session", "account"])
        self.assertTrue(issubclass(guard, Guard))

    def test_internal_security(self):
        self.response.request.account["type"] = "internal"

        result = self.guard.resolve(self.response)

        self.assertFalse(result)

    def test_account_authorization(self):
        self.response.request.account = {"type": "account", "login": "login", "password": "password"}

        result = self.guard.resolve(self.response)

        self.assertTrue(result)

    def test_account_authorization_bad_pass(self):
        self.response.request.account = {"type": "account", "login": "login", "password": "wrong"}

        result = self.guard.resolve(self.response)

        self.assertFalse(result)



