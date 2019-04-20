from Requests.RequestInterface import Request
from Responses.BasicResponse import BasicResponse
from Responses.ResponseGeneratorInterface import ResponseGenerator


class BasicResponseGenerator(ResponseGenerator):
    def __init__(self, forwarders: []):
        super().__init__(forwarders)
        self.response_type = BasicResponse

    def generate(self, request: Request):
        return self.response_type("new", request)
