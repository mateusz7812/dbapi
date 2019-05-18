from Guards.GuardInterface import Guard


class BasicGuard(Guard):
    authorization_methods = ["session", "account"]

    def resolve(self, response):
        authorized = False

        if response.request.account["type"] == "account":
            if response.request.account["password"] == "password":
                authorized = True

        return authorized
