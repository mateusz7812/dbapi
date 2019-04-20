class Response:
    def __init__(self, status="none", request=None):
        self.status = status
        self.request = request
        self.required_requests = []

    def to_dict(self):
        raise NotImplementedError
