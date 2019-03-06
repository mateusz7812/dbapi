from unittest import TestCase

from RedisManager import RExecutor


class TestRedisConnections(TestCase):
    def test_basic(self):
        RExecutor()
