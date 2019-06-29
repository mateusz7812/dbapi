import copy

from Guards.GuardInterface import Guard
from Requests.Request import Request
from Responses.Response import BasicResponse


class Authorizer(Guard):
    def __init__(self):
        super().__init__()
        self.authorization_methods = ["anonymous", "session", "account", "admin"]
        self.processors = {}

    def resolve(self, response):
        if self.verify_account(response.request.account):
            if self.verify_action_requirements(response.request):
                self.get_account(response.request)
                response.status = "authorized"
                return response
            else:
                response.status = "not authorized action"
        else:
            response.status = "not authorized account"
        return response

    def verify_action_requirements(self, request):
        processor = self.find_processor(request)
        needed_fields_sets = processor.authorization_rules[request.action][request.account["type"]]

        request_fields = copy.deepcopy(request.object)
        request_fields.pop("type")

        for needed_fields in needed_fields_sets:
            if needed_fields.issubset(set(request_fields.keys())):
                return True

        return False

    def get_account(self, request):
        if request.account["type"] == "account" or request.account["type"] == "admin":
            taken_response = self.processors["account"].process(
                BasicResponse("new", Request({"type": "internal"},
                                             {"type": "account", "login": request.account["login"],
                                              "password": request.account["password"]}, "get")))
            request.account = taken_response.result["objects"][0]
        elif request.account["type"] == "session":
            taken_response = self.processors["account"].process(
                BasicResponse("new", Request({"type": "internal"},
                                             {"type": "account", "id": request.account["user_id"]}, "get")))
            request.account = taken_response.result["objects"][0]
        return request

    def find_processor(self, request):
        try:
            return self.processors[request.object["type"]]
        except KeyError:
            raise Exception("No processor with such name")

    def verify_account(self, response_account):
        if response_account["type"] == "anonymous":
            return True

        elif response_account["type"] == "account" or response_account["type"] == "admin":
            account_response = BasicResponse("new", Request({"type": "internal"},
                                                            {"type": "account", "login": response_account["login"],
                                                             "password": response_account["password"]}, "get"))
            accounts = self.processors["account"].process(account_response).result["objects"]
            if len(accounts) == 1:
                if response_account["type"] == "account":
                    return True

                elif response_account["type"] == "admin":
                    if accounts[0]["account_type"] == "admin":
                        return True

        elif response_account["type"] == "session":
            session_response = BasicResponse("new", Request({"type": "internal"}, {"type": "session", "user_id":
                response_account["user_id"]}, "get"))
            sessions = self.processors["session"].process(session_response).result["objects"]
            keys = [session["key"] for session in sessions]
            if response_account["key"] in keys:
                return True

        return False
