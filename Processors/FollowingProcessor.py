import copy

from Processors.ProcessorInterface import Processor


class FollowingProcessor(Processor):
    name = "follow"

    authorization_rules = {
        "add": {"anonymous": [], "account": [{"followed"}], "session": [{"followed"}], "admin": [set()]},
        "get": {"anonymous": [], "account": [{"followed"}, {"follower"}],
                "session": [{"followed"}, {"follower"}], "admin": [set()]},
        "del": {"anonymous": [], "account": [{"followed"}], "session": [{"followed"}],
                "admin": [set()]}}

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if response.request.action == "add":
            if "follower" not in data.keys():
                data["follower"] = response.request.account["id"]

        response.result["objects"] = self.manager.manage(response.request.action, data)
        response.status = "handled"
        return response
