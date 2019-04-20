from Requests.RequestInterface import Request
from Responses.BasicResponse import BasicResponse
from Responses.ResponseGeneratorInterface import ResponseGenerator


class BasicResponseGenerator(ResponseGenerator):
    def __init__(self):
        super().__init__()
        self.response_class = BasicResponse

    def generate(self, request: Request):
        return self.response_class("new", request)
