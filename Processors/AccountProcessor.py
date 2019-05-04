import copy

from Processors.ProcessorInterface import Processor


class AccountProcessor(Processor):
    name = "account"

    def get_required_requests(self, response):
        return []

    def process(self, response):
        data = copy.deepcopy(response.request.object)
        data.pop("type")

        if not ("login" in data.keys() and "password" in data.keys()):
            response.status = "failed"
            response.result["error"] = "no login/password"
            return response

        if response.request.action == "add":
            same_login_users = self.managers[0].manage("get", {"login": data["login"]})
            if same_login_users:
                response.status = "failed"
                response.result["error"] = "taken login"
                return response

            if "nick" in data.keys():
                same_nick_users = self.managers[0].manage("get", {"nick": data["nick"]})
                if same_nick_users:
                    response.status = "failed"
                    response.result["error"] = "taken nick"
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
