from unittest import TestCase

from SessionManager import RExecutor


class TestRedisConnections(TestCase):
    def test_basic(self):
        RExecutor()
