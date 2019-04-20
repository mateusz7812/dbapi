from Requests.RequestInterface import Request


class RequestGenerator:
    def __init__(self):
        self.request_type = None

    def generate(self, data: {}):
        raise NotImplementedError

