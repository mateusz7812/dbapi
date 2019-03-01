import json
from unittest import TestCase
import requests


class TestServer(TestCase):
    def test_connect_exist(self):
        r = requests.get("http://localhost:8080")
        self.assertEqual(r.status_code, 200)

    def test_new_user_procedure(self):
        # previous user is being deleted
        response = self.get_response(['user', 'del', 'login', 'password'])
        self.assertEqual(response, True)

        # user is being registered
        response = self.get_response(['user', 'reg', 'login', 'password', 'nick'])
        self.assertEqual(response, True)

        # user is being logged in
        response = self.get_response(['user', 'log', 'login', 'password'])
        self.assertNotEqual(response, -1)

        user_id, user_key = response

        # lists are being showed
        response = self.get_response(['list', 'get', user_id, user_key])
        self.assertEqual(response, [])

        # list is being added
        response = self.get_response(['list', 'add', user_id, user_key, 'testowa', 'content'])
        self.assertNotEqual(response, -1)

        list_id = response

        # added list exist is being checked
        response = self.get_response(['list', 'get', user_id, user_key])
        self.assertEqual(response, [['testowa', 'content']])

        # list is being deleted
        response = self.get_response(['list', 'del', user_id, user_key, list_id])
        self.assertEqual(response, True)

        # lists are being showed
        response = self.get_response(['list', 'get', user_id, user_key])
        self.assertEqual(response, [])

        # user is being logged out
        response = self.get_response(['user', 'logout', user_id, user_key])
        self.assertNotEqual(response, -1)

        # list is being added, but it end bad
        response = self.get_response(['list', 'add', user_id, user_key, 'testowa', 'content'])
        self.assertEqual(response, -1)

    def get_response(self, data):
        r = requests.post("http://localhost:8080", data=json.dumps(data))
        return r.content
