
from Requests.Request import Request
from Requests.RequestGeneratorInterface import RequestGeneratorInterface


class RequestGenerator(RequestGeneratorInterface):
    def __init__(self):
        super().__init__()
        self.request_type = Request

    def generate(self, data: {}):
        data_object = data["object"]
        account_object = data["account"]
        new_request = self.request_type(account_object, data_object, data["action"])
        return new_request
