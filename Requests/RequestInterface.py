from Objects.ObjectInterface import Object


class Request:
    def __init__(self, account: Object, object: Object, action: str):
        if account.type == "account":
            self.account = account
        self.object = object
        self.action = action

    def validate(self):
        raise NotImplementedError
