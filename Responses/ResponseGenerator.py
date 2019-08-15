from Requests.Request import Request
from Responses.Response import Response
from Responses.ResponseGeneratorInterface import ResponseGeneratorInterface


class ResponseGenerator(ResponseGeneratorInterface):
    def __init__(self):
        super().__init__()
        self.response_class = Response

    def generate(self, request: Request):
        return self.response_class("new", request)
