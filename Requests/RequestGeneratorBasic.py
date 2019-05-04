
from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorInterface import RequestGenerator


class BasicRequestGenerator(RequestGenerator):
    def __init__(self):
        super().__init__()
        self.request_type = BasicRequest

    def generate(self, data: {}):
        data_object = data["object"]
        account_object = data["account"]
        new_request = self.request_type(account_object, data_object, data["action"])
        return new_request
