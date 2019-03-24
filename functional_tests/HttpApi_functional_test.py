import json
import os
from unittest import TestCase
import requests


def clear_file(name):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    cur_dir = "\\".join(cur_dir.split("\\")[:-1])
    with open(cur_dir + "\\textDataBases\\" + name, "r") as f:
        config = f.readline()
    with open(cur_dir + "\\textDataBases\\" + name, "w") as f:
        f.truncate()
        f.write(config)


class TestServer(TestCase):
    def setUp(self):
        clear_file("users")
        clear_file("salts")
        clear_file("passwords")
        clear_file("temp")
        clear_file("lists")

    def get_response(self, data):
        r = requests.post("http://localhost:8080", data=json.dumps(data))
        if r.content:
            return json.loads(str(r.content, "utf-8"))
        else:
            raise Exception("lack of data")

    def test_connect_exist(self):
        r = requests.get("http://127.0.0.1:8080")
        self.assertEqual(r.status_code, 200)

    def test_new_user_procedure(self):
        # user is being registered
        response = self.get_response(
            {"object": 'user', "action": 'reg',
             "login": 'login', "password": 'password', "nick": 'nick'})
        self.assertEqual("user added", response["info"])

        # user is being logged in
        response = self.get_response(
            {"object": 'user', "action": 'login',
             "login": 'login', "password": 'password'})
        self.assertEqual("session added", response["info"])
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
        self.assertEqual(int, type(response["id"]))
        list_id = response["id"]

        # added list exist is being checked
        response = self.get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(response["lists"],
                         [{"user_id": user_id, "id": list_id, "name": 'testowa', "content": 'content'}])

        # list is being edited
        response = self.get_response(
            {"object": "list", "action": "edit",
             "user_id": user_id, "user_key": user_key,
             "list_id": list_id, "name": 'name', "content": 'content'})
        self.assertEqual(response["info"], "list edited")

        # edited list exist is being checked
        response = self.get_response(
            {"object": 'list', "action": 'get',
             "user_id": user_id, "user_key": user_key})
        self.assertEqual(response["info"], "lists gotten")
        self.assertEqual(1, len(response["lists"]))
        self.assertEqual(response["lists"][0]["name"], 'name')

        # list is being deleted
        response = self.get_response(
            {"object": 'list', "action": 'del',
             "user_id": user_id, "user_key": user_key,
             "name": 'name'})
        self.assertEqual("lists deleted", response["info"])

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
        self.assertEqual("session deleted", response["info"])

        # list is being added, but it end bad
        response = self.get_response(
            {"object": 'list', "action": 'add',
             "user_id": user_id, "user_key": user_key,
             "name": 'testowa', "content": 'content'})
        self.assertEqual("session not correct", response["info"])

        # user is being logged in
        response = self.get_response(
            {"object": 'user', "action": 'login',
             "login": 'login', "password": 'password'})
        self.assertEqual("session added", response["info"])
        self.assertEqual(int, type(response["user_id"]))
        self.assertEqual(str, type(response["user_key"]))
        user_id = response["user_id"]
        user_key = response["user_key"]

        # user is being deleted
        response = self.get_response(
            {"object": 'user', "action": 'delete',
             "user_id": user_id, "user_key": user_key,
             "login": 'login', "password": 'password'})
        self.assertIn(response["info"], ["user deleted"])
