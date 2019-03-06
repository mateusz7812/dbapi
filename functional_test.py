import json
from unittest import TestCase
import requests


class TestServer(TestCase):
    def test_connect_exist(self):
        r = requests.get("http://127.0.0.1:8080")
        self.assertEqual(r.status_code, 200)

    def test_new_user_procedure(self):
        # previous user is being deleted
        response = self.get_response(['user', 'del', 'login', 'password'])
        self.assertIn(response, ["user deleted", "user not found"])

        # user is being registered
        response = self.get_response(['user', 'reg', 'login', 'password', 'nick'])
        self.assertEqual(response, "user added")

        # user is being logged in
        response = self.get_response(['user', 'log', 'login', 'password'])
        self.assertEqual(response[0], "user logged in")
        [user_id, user_key] = response[1:3]

        # lists are being showed
        response = self.get_response(['list', 'get', user_id, user_key])
        self.assertEqual(response[0], "lists gotten")
        self.assertEqual(response[1], [])

        # list is being added
        response = self.get_response(['list', 'add', user_id, user_key, 'testowa', 'content'])
        self.assertEqual(response[0], "list added")
        list_id = response[1]

        # added list exist is being checked
        response = self.get_response(['list', 'get', user_id, user_key])
        self.assertEqual(response[0], "lists gotten")
        self.assertEqual(response[1], [['testowa', 'content']])

        # list is being deleted
        response = self.get_response(['list', 'del', user_id, user_key, list_id])
        self.assertEqual(response, "list deleted")

        # lists are being showed
        response = self.get_response(['list', 'get', user_id, user_key])
        self.assertEqual(response[0], "lists gotten")
        self.assertEqual(response[1], [])

        # user is being logged out
        response = self.get_response(['user', 'logout', user_id, user_key])
        self.assertEqual(response, "user logged out")

        # list is being added, but it end bad
        response = self.get_response(['list', 'add', user_id, user_key, 'testowa', 'content'])
        self.assertEqual(response, "user not logged in")

    def get_response(self, data):
        r = requests.post("http://localhost:8080", data=json.dumps(data))
        return str(r.content)
