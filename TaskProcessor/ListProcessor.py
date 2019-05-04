import copy

from Requests.BasicRequest import BasicRequest
from TaskProcessor.ProcessorInterface import Processor


class ListProcessor(Processor):
    name = "list"

    def get_required_requests(self, response):
        return [BasicRequest({"type": "internal"}, {"type": "account", "login": response.request.account["login"],
                                                    "password": response.request.account["password"]}, "get")]

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if len(response.request.required["account"]) != 1:
            response.status = "failed"
            response.result["error"] = "user not found"
            return response

        data["user_id"] = response.request.required["account"][0]["id"]

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
