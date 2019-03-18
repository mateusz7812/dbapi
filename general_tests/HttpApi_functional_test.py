import json
from unittest import TestCase
import requests


class TestServer(TestCase):
    def test_connect_exist(self):
        r = requests.get("http://127.0.0.1:8080")
        self.assertEqual(r.status_code, 200)

    def test_new_user_procedure(self):
        # previous user is being deleted
        response = self.get_response(
            {"object": 'user', "action": 'del',
             "login": 'login', "password": 'password'})
        self.assertIn(response["info"], ["user deleted", "user not found"])

        # user is being registered
        response = self.get_response(
            {"object": 'user', "action": 'reg',
             "login": 'login', "password": 'password', "nick": 'nick'})
        self.assertEqual(response["info"], "user added")

        # user is being logged in
        response = self.get_response(
            {"object": 'user', "action": 'login',
             "login": 'login', "password": 'password'})
        self.assertEqual(response["info"], "user logged in")
        self.assertEqual(int, type(response["user_id"]))
        self.assertEqual(str, type(response["user_key"]))
        user_id = response["user_id"]
        user_key = response["user_key"]

        # lists are being showed
        response = self.get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(response["lists"], [])

        # list is being added
        response = self.get_response(
            {"object": 'list', "action": 'add',
             "user_id": user_id, "user_key": user_key,
             "name": 'testowa', "content": 'content'})
        self.assertEqual(response["info"], "list added")
        self.assertEqual(int, type(response["list_id"]))
        list_id = response["list_id"]

        # added list exist is being checked
        response = self.get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(response["lists"], [{"list_id": list_id, "name": 'testowa', "content": 'content'}])

        # list is being deleted
        response = self.get_response(
            {"object": 'list', "action": 'del',
             "user_id": user_id, "user_key": user_key,
             "list_id": list_id})
        self.assertEqual(response["info"], "list deleted")

        # lists are being showed
        response = self.get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(response["lists"], [])

        # user is being logged out
        response = self.get_response(
            {"object": 'user', "action": 'logout',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "user logged out")

        # list is being added, but it end bad
        response = self.get_response(
            {"object": 'list', "action": 'add',
             "user_id": user_id, "user_key": user_key,
             "name": 'testowa', "content": 'content'})
        self.assertEqual(response["info"], "user not logged in")

    def get_response(self, data):
        r = requests.post("http://localhost:8080", data=json.dumps(data))
        return str(r.content, "utf-8")
