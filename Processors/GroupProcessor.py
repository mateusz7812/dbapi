import copy

from Processors.ProcessorInterface import Processor


class GroupProcessor(Processor):
    name = "group"

    authorization_rules = {
        "add": {"anonymous": [], "account": [set()], "session": [set()], "admin": [set()]},
        "get": {"anonymous": [], "account": [set()], "session": [set()], "admin": [set()]},
        "del": {"anonymous": [], "account": [{"id"}], "session": [{"id"}], "admin": [set()]}}

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if response.request.action == "add":
            if "name" not in data.keys():
                response.status = "failed"
                response.result["error"] = "name not found"
                return response

            same_name_groups = self.manager.manage("get", {"name": data["name"]})
            if same_name_groups:
                response.status = "failed"
                response.result["error"] = "taken name"
                return response

            if "id" not in data.keys():
                rows = self.manager.manage("get", {})
                if len(rows):
                    row = rows[-1]
                    last_id = row["id"]
                else:
                    last_id = 0
                data["id"] = last_id + 1

            if "admin_id" not in data.keys():
                data["admin_id"] = response.request.account["id"]

        if response.request.action == "del":
            if "id" not in data.keys():
                response.status = "failed"
                response.result["error"] = "no id"
                return response

            if "account_type" not in response.request.account:
                id_groups = self.manager.manage("get", {"id": data["id"], "name": data["name"]})
                if not id_groups:
                    response.status = "failed"
                    response.result["error"] = "bad group id"
                    return response

                admin_id = id_groups[0]["admin_id"]
                if admin_id != response.request.account["id"]:
                    response.status = "failed"
                    response.result["error"] = "bad account id"
                    return response
            else:
                if response.request.account["account_type"] != "admin":
                    raise NotImplementedError

        response.result["objects"] = self.manager.manage(response.request.action, data)
        response.status = "handled"
        return response
