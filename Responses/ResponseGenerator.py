from Requests.RequestInterface import Request
from Responses.Response import BasicResponse
from Responses.ResponseGeneratorInterface import ResponseGenerator


class ResponseGenerator(ResponseGenerator):
    def __init__(self):
        super().__init__()
        self.response_class = BasicResponse

    def generate(self, request: Request):
        return self.response_class("new", request)
