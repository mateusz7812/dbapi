from unittest import TestCase

import requests

from Tests.functions_for_tests import clear_file, get_response


class TestServer(TestCase):
    def setUp(self):
        clear_file("users")
        clear_file("salts")
        clear_file("passwords")
        clear_file("temp")
        clear_file("lists")

    def test_connect_exist(self):
        r = requests.get("http://127.0.0.1:8080")
        self.assertEqual(r.status_code, 200)

    def test_new_user_procedure(self):
        # user is being registered
        response = get_response(
            {"object": 'user', "action": 'reg',
             "login": 'login', "password": 'password', "nick": 'nick'})
        self.assertEqual("user added", response["info"])

        # user is being logged in
        response = get_response(
            {"object": 'user', "action": 'login',
             "login": 'login', "password": 'password'})
        self.assertEqual("session added", response["info"])
        self.assertEqual(int, type(response["user_id"]))
        self.assertEqual(str, type(response["user_key"]))
        user_id = response["user_id"]
        user_key = response["user_key"]

        # lists are being showed
        response = get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(response["lists"], [])

        # list is being added
        response = get_response(
            {"object": 'list', "action": 'add',
             "user_id": user_id, "user_key": user_key,
             "name": 'testowa', "content": 'content'})
        self.assertEqual(response["info"], "list added")
        self.assertEqual(int, type(response["id"]))
        list_id = response["id"]

        # added list exist is being checked
        response = get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(response["lists"],
                         [{"user_id": user_id, "id": list_id, "name": 'testowa', "content": 'content'}])

        # list is being edited
        response = get_response(
            {"object": "list", "action": "edit",
             "user_id": user_id, "user_key": user_key,
             "list_id": list_id, "name": 'name', "content": 'content'})
        self.assertEqual(response["info"], "list edited")

        # edited list exist is being checked
        response = get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(1, len(response["lists"]))
        self.assertEqual(response["lists"][0]["name"], 'name')

        # list is being deleted
        response = get_response(
            {"object": 'list', "action": 'del',
             "user_id": user_id, "user_key": user_key,
             "name": 'name'})
        self.assertEqual("lists deleted", response["info"])

        # lists are being showed
        response = get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(response["lists"], [])

        # user is being logged out
        response = get_response(
            {"object": 'user', "action": 'logout',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual("session deleted", response["info"])

        # list is being added, but it end bad
        response = get_response(
            {"object": 'list', "action": 'add',
             "user_id": user_id, "user_key": user_key,
             "name": 'testowa', "content": 'content'})
        self.assertEqual("session not correct", response["info"])

        # user is being logged in
        response = get_response(
            {"object": 'user', "action": 'login',
             "login": 'login', "password": 'password'})
        self.assertEqual("session added", response["info"])
        self.assertEqual(int, type(response["user_id"]))
        self.assertEqual(str, type(response["user_key"]))
        user_id = response["user_id"]
        user_key = response["user_key"]

        # user is being deleted
        response = get_response(
            {"object": 'user', "action": 'delete',
             "user_id": user_id, "user_key": user_key,
             "login": 'login', "password": 'password'})
        self.assertIn(response["info"], ["user deleted"])
