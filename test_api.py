import psycopg2 as psycopg2
from twisted.trial import unittest
from twisted.web.client import Agent, readBody
from twisted.internet import reactor
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer
from io import BytesIO
import json


class TestServer(unittest.TestCase):

    def setUp(self):
        self.api = Agent(reactor)

    def tearDown(self):
        self.api = None

    def test_user(self):
        data = json.dumps(['user', 'register', 'login', 'password'])
        ret = bytes(json.dumps(['register']), "utf-8")
        body = FileBodyProducer(BytesIO(bytes(data, "utf-8")))

        response = self.make_response(body)
        response.addCallback(readData)

        response.addCallback(lambda x: self.assertEqual(x, ret))
        return response

    def test_list(self):
        data = json.dumps(['list', 'add', 'name', 'content'])
        ret = bytes(json.dumps(['add']), "utf-8")
        body = FileBodyProducer(BytesIO(bytes(data, "utf-8")))

        response = self.make_response(body)
        response.addCallback(readData)

        response.addCallback(lambda x: self.assertEqual(x, ret))
        return response

    def make_response(self, body):
        return self.api.request(
            bytes('POST', 'utf8'),
            bytes('http://localhost:8080', 'utf8'),
            Headers({'User-Agent': ['Twisted Web Client Example']}),
            body)


class TestDataBase(unittest.TestCase):
    def test_connection_exist(self):
        try:
            conn = psycopg2.connect(host="localhost:5432", database="lists", user="admin", password="admin")
            conn.close()

            conn = psycopg2.connect(host="localhost:5432", database="users", user="admin", password="admin")
            conn.close()
        except Exception:
            self.fail()

    def test_user_exist(self):
        with psycopg2.connect(host="localhost:5432", database="users", user="admin", password="admin") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * from users")


def readData(res):
    body = readBody(res)
    return body
