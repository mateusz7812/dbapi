import copy
import random

from Processors.ProcessorInterface import Processor


class SessionProcessor(Processor):
    name = "session"
    authorization_rules = {
        "add": {"anonymous": [], "account": [{"user_id"}], "session": [{"user_id"}], "admin": [set()]},
        "get": {"anonymous": [], "account": [{"user_id"}],
                "session": [{"user_id"}], "admin": [set()]},
        "del": {"anonymous": [], "account": [{"user_id"}], "session": [{"user_id"}],
                "admin": [set()]}}

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if response.request.action == "add":
            if "key" not in data.keys():
                key = random.randint(1000000000000000000000000,
                                     9999999999999999999999999)
                data["key"] = str(key)
            while self.manager.manage("get", {"key": data["key"]}):
                key = random.randint(1000000000000000000000000,
                                     9999999999999999999999999)
                data["key"] = str(key)

        response.result["objects"] = self.manager.manage(response.request.action, data)
        response.status = "handled"
        return response
