import copy

from Requests.BasicRequest import BasicRequest
from Processors.ProcessorInterface import Processor


class ListProcessor(Processor):
    name = "list"

    authorization_rules = {
        "add": {"anonymous": [], "account": [{"name"}], "session": [{"name"}], "admin": [set()]},
        "get": {"anonymous": [], "account": [{"user_id"}],
                "session": [{"user_id"}], "admin": [set()]},
        "del": {"anonymous": [], "account": [{"user_id", "id", "name"}], "session": [{"user_id", "id", "name"}],
                "admin": [set()]}}

    def get_required_requests(self, response):
        if response.request.account["type"] == "account":
            return [BasicRequest({"type": "internal"}, {"type": "account", "login": response.request.account["login"],
                                                        "password": response.request.account["password"]}, "get")]
        return []

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if response.request.account["type"] == "account":
            data["user_id"] = response.request.required["account"]["objects"][0]["id"]
        elif response.request.account["type"] == "session":
            data["user_id"] = response.request.account["user_id"]

        if response.request.action == "add":
            if "name" not in data.keys():
                response.status = "failed"
                response.result["error"] = "name not found"
                return response

            same_name_lists = self.managers[0].manage("get", {"user_id": data["user_id"], "name": data["name"]})
            if same_name_lists:
                response.status = "failed"
                response.result["error"] = "taken name"
                return response

            if "id" not in data.keys():
                rows = self.managers[0].manage("get", {})
                if len(rows):
                    row = rows[0]
                    last_id = row["id"]
                else:
                    last_id = 0
                data["id"] = last_id + 1

        response.result["objects"] = self.managers[0].manage(response.request.action, data)
        response.status = "handled"
        return response
