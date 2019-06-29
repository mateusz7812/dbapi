from unittest import TestCase
from unittest.mock import Mock

from Processors.FollowingProcessor import FollowingProcessor
from Requests.Request import Request
from Requests.RequestGenerator import RequestGenerator
from Responses.Response import BasicResponse

processor = FollowingProcessor
request_generator = RequestGenerator


class TestFollowingProcessor(TestCase):
    def setUp(self):
        self.processor = processor()

        self.response = BasicResponse("", Request({}, {}, ""))

    def test_options(self):
        self.assertEqual("follow", self.processor.name)

    def test_add(self):
        self.response.request.account = {"id": 3}
        self.response.request.object = {"type": "follow", "followed": 4}
        self.response.request.action = "add"

        manager = Mock()
        manager.manage.return_value = True
        self.processor.manager = manager

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)
        manager.manage.assert_called_with("add", {"follower": 3, "followed": 4})

    def test_get(self):
        self.response.request.account = {"id": 3}
        self.response.request.object = {"type": "follow"}
        self.response.request.action = "get"

        manager = Mock()
        manager.manage.return_value = [{"follower": 3, "followed": 4}, {"follower": 3, "followed": 8},
                                       {"follower": 3, "followed": 10}]
        self.processor.manager = manager

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)
        manager.manage.assert_called_with("get", {})
        self.assertEqual([{"follower": 3, "followed": 4}, {"follower": 3, "followed": 8},
                          {"follower": 3, "followed": 10}], taken_response.result["objects"])

    def test_del(self):
        self.response.request.account = {"id": 3}
        self.response.request.object = {"type": "follow"}
        self.response.request.action = "del"

        manager = Mock()
        manager.manage.return_value = [{"follower": 3, "followed": 4}, {"follower": 3, "followed": 8},
                                       {"follower": 3, "followed": 10}]
        self.processor.manager = manager

        taken_response = self.processor.process(self.response)

        self.assertEqual("handled", taken_response.status)
        manager.manage.assert_called_with("del", {"follower": 3})
        self.assertEqual([{"follower": 3, "followed": 4}, {"follower": 3, "followed": 8},
                          {"follower": 3, "followed": 10}], taken_response.result["objects"])
