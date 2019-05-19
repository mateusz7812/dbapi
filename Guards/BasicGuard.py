from Guards.GuardInterface import Guard
from Requests.BasicRequest import BasicRequest
from Responses.BasicResponse import BasicResponse


class BasicGuard(Guard):
    authorization_methods = ["session", "account", "admin"]
    processors = {}

    def resolve(self, response):
        if response.request.account["type"] == "account" or response.request.account["type"] == "admin":
            account_response = BasicResponse("new", BasicRequest({"type": "internal"}, {"type": "account", "login":
                                             response.request.account["login"]}, "get"))
            accounts = self.processors["account"].process(account_response)
            if len(accounts) == 1:
                if response.request.account["password"] == accounts[0]["password"]:

                    if response.request.account["type"] == "account":
                        return True

                    elif response.request.account["type"] == "admin":
                        admin_response = BasicResponse("new",
                                                       BasicRequest({"type": "internal"}, {"type": "admin", "user_id":
                                                                    accounts[0]["id"]}, "get"))
                        admins = self.processors["admin"].process(admin_response)
                        if len(admins) == 1:
                            return True

        elif response.request.account["type"] == "session":
            session_response = BasicResponse("new", BasicRequest({"type": "internal"}, {"type": "session", "user_id":
                                             response.request.account["user_id"]}, "get"))
            sessions = self.processors["session"].process(session_response)
            keys = [session["key"] for session in sessions]
            if response.request.account["key"] in keys:
                return True

        return False
