from Requests.Request import Request


class ResponseGeneratorInterface:
    def __init__(self):
        self.response_class = None

    def generate(self, request: Request):
        raise NotImplementedError
