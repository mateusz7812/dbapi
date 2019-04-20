from Requests.RequestInterface import Request


class ResponseGenerator:
    def __init__(self):
        self.response_class = None

    def generate(self, request: Request):
        raise NotImplementedError
