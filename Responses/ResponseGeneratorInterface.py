from Requests.RequestInterface import Request


class ResponseGenerator:
    def __init__(self, forwarders: []):
        self.forwarders = forwarders
        self.response_type = None

    def generate(self, request: Request):
        raise NotImplementedError
