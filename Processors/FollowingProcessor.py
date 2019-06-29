import copy

from Processors.ProcessorInterface import Processor


class FollowingProcessor(Processor):
    name = "follow"

    authorization_rules = {
        "add": {"anonymous": [], "account": [{"followed", "following"}], "session": [{"followed", "following"}],
                "admin": [{"following"}]},
        "get": {"anonymous": [], "account": [{"id", "following"}, {"followed", "following"}, {"follower", "following"}],
                "session": [{"id", "following"}, {"followed", "following"}, {"follower", "following"}],
                "admin": [{"following"}]},
        "del": {"anonymous": [], "account": [{"followed", "following"}], "session": [{"followed", "following"}],
                "admin": [{"following"}]}}

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if response.request.action == "add" or response.request.action == "del":
            if "follower" not in data.keys():
                data["follower"] = response.request.account["id"]

        response.result["objects"] = self.manager.manage(response.request.action, data)
        response.status = "handled"
        return response
