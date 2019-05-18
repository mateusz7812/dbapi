import copy
import random

from Processors.ProcessorInterface import Processor
from Requests.BasicRequest import BasicRequest


class SessionProcessor(Processor):
    name = "session"

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")
        if len(response.request.required["account"]["objects"]) != 1:
            response.status = "failed"
            response.result["error"] = "user not found"
            return response

        data["user_id"] = response.request.required["account"]["objects"][0]["id"]

        if response.request.action == "add":
            if "key" not in data.keys():
                key = random.randint(1000000000000000000000000,
                                     9999999999999999999999999)
                data["key"] = str(key)
            while self.managers[0].manage("get", {"key": data["key"]}):
                key = random.randint(1000000000000000000000000,
                                     9999999999999999999999999)
                data["key"] = str(key)
            if self.managers[0].manage(response.request.action, data):
                response.result["objects"] = [data]

        elif response.request.action == "get":
            response.result["objects"] = []
            keys = [row["key"] for row in self.managers[0].manage(response.request.action, data)]
            if response.request.account["key"] in keys:
                response.result["objects"] = response.request.required["account"]["objects"]

        elif response.request.action == "del":
            response.result["objects"] = self.managers[0].manage(response.request.action, data)

        response.status = "handled"
        return response

    def get_required_requests(self, response):
        if response.request.action == "add":
            return [BasicRequest({"type": "internal"}, {"type": "account", "login": response.request.account["login"],
                                                        "password": response.request.account["password"]}, "get")]
        elif response.request.action == "get" or response.request.action == "del":
            return [
                BasicRequest({"type": "internal"}, {"type": "account", "id": response.request.account["user_id"]},
                             "get")]
