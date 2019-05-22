import copy

from Guards.GuardInterface import Guard
from Requests.BasicRequest import BasicRequest
from Responses.BasicResponse import BasicResponse


class BasicGuard(Guard):
    def __init__(self):
        super().__init__()
        self.authorization_methods = ["anonymous", "session", "account", "admin"]
        self.processors = {}

    def resolve(self, response):
        if self.verify_account(response.request.account):
            return self.verify_action_requirements(response.request)
        return False

    def verify_action_requirements(self, request):
        processor = self.find_processor(request)
        needed_fields_sets = processor.authorization_rules[request.action][request.account["type"]]

        for needed_fields in needed_fields_sets:
            request_fields = copy.deepcopy(request.object)
            request_fields.pop("type")

            if needed_fields.issubset(set(request_fields.keys())):
                return True

        return False

    def find_processor(self, request):
        try:
            return self.processors[request.object["type"]]
        except KeyError:
            raise Exception("No processor with such name")

    def verify_account(self, response_account):
        if response_account["type"] == "anonymous":
            return True

        elif response_account["type"] == "account" or response_account["type"] == "admin":
            account_response = BasicResponse("new", BasicRequest({"type": "internal"}, {"type": "account", "login":
                                             response_account["login"]}, "get"))
            accounts = self.processors["account"].process(account_response).result["objects"]
            if len(accounts) == 1:
                if response_account["password"] == accounts[0]["password"]:

                    if response_account["type"] == "account":
                        return True

                    elif response_account["type"] == "admin":
                        if accounts[0]["account_type"] == "admin":
                            return True

        elif response_account["type"] == "session":
            session_response = BasicResponse("new", BasicRequest({"type": "internal"}, {"type": "session", "user_id":
                                             response_account["user_id"]}, "get"))
            sessions = self.processors["session"].process(session_response).result["objects"]
            keys = [session["key"] for session in sessions]
            if response_account["key"] in keys:
                return True

        return False
