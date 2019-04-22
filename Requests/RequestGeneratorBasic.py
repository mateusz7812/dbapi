
from Requests.BasicRequest import BasicRequest
from Requests.RequestGeneratorInterface import RequestGenerator


class BasicRequestGenerator(RequestGenerator):
    def __init__(self):
        super().__init__()
        self.request_type = BasicRequest

    def generate(self, data: {}):
        dataObject = data["object"]
        accountObject = data["account"]
        new_request = self.request_type(accountObject, dataObject, data["action"])
        return new_request
