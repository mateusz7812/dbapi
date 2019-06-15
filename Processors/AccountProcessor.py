import copy

from Processors.ProcessorInterface import Processor


class AccountProcessor(Processor):
    name = "account"
    authorization_rules = {
        "add": {"anonymous": [{"login", "password"}], "account": [], "session": [], "admin": [set()]},
        "get": {"anonymous": [{"login", "password"}], "account": [{"nick"}, {"id"}, {"login", "password"}],
                "session": [{"nick"}, {"id"}, {"login", "password"}], "admin": [set()]},
        "del": {"anonymous": [{"login", "password"}], "account": [{"login", "password"}], "session": [],
                "admin": [set()]}}

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if response.request.action == "add":
            if "login" not in data.keys():
                response.status = "failed"
                response.result["error"] = "login not found"
                return response

            if "password" not in data.keys():
                response.status = "failed"
                response.result["error"] = "password not found"
                return response

            same_login_users = self.manager.manage("get", {"login": data["login"]})
            if same_login_users:
                response.status = "failed"
                response.result["error"] = "taken login"
                return response

            if "nick" in data.keys():
                same_nick_users = self.manager.manage("get", {"nick": data["nick"]})
                if same_nick_users:
                    response.status = "failed"
                    response.result["error"] = "taken nick"
                    return response

            if "id" not in data.keys():
                rows = self.manager.manage("get", {})
                if len(rows):
                    row = rows[-1]
                    last_id = row["id"]
                else:
                    last_id = 0
                data["id"] = last_id + 1

            if "account_type" in data.keys():
                admins = self.manager.manage("get", {"account_type": "admin"})
                if len(admins):
                    if response.request.account["type"] != "admin":
                        response.status = "failed"
                        response.result["error"] = "first admin added"
                        return response

        response.result["objects"] = self.manager.manage(response.request.action, data)
        response.status = "handled"
        if response.request.action == "get":
            for one_object in response.result["objects"]:
                one_object.pop("password")
        return response
